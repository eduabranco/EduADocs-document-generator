from llm_handlers.api_handler import get_llm_response
from docx import Document
import io

def generate_summary(params):
    """Generate summary document"""
    
    prompt = _build_summary_prompt(params)
    
    try:
        # Get content from LLM
        content = get_llm_response(prompt, params["llm_config"])
        
        # Create Word document
        docx_file = _create_summary_docx(content, params)
        
        return {
            "success": True,
            "content": content,
            "docx_file": docx_file
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def _build_summary_prompt(params):
    """Build prompt for summary generation"""
    
    prompt = f"""
    Create a comprehensive summary for {params['subject']} at {params['grade_level']} level.
    
    Topic: {params['topic']}
    Length: {params['summary_length']}
    Format: {params['format_style']}
    Include examples: {params['include_examples']}
    
    Structure the summary with:
    1. Introduction to the topic
    2. Main concepts and key points
    3. {'Real-world examples and applications' if params['include_examples'] else 'Theoretical explanations'}
    4. Summary of key takeaways
    5. Suggested further reading or activities
    
    Make sure the content is:
    - Age-appropriate for {params['grade_level']}
    - Well-organized and easy to follow
    - Educationally comprehensive
    - Formatted according to {params['format_style']} style
    """
    
    return prompt

def _create_summary_docx(content, params):
    """Create Word document from summary content"""
    
    doc = Document()
    
    # Title
    title = doc.add_heading(f"{params['subject']} - Summary", 0)
    title.alignment = 1  # Center alignment
    
    # Subtitle
    doc.add_heading(f"Topic: {params['topic']}", level=2)
    doc.add_heading(f"Grade Level: {params['grade_level']}", level=3)
    
    # Add content based on format style
    if params['format_style'] == "Bullet Points":
        _add_bullet_content(doc, content)
    elif params['format_style'] == "Outline":
        _add_outline_content(doc, content)
    elif params['format_style'] == "Q&A Format":
        _add_qa_content(doc, content)
    else:  # Paragraphs
        _add_paragraph_content(doc, content)
    
    # Save to bytes
    doc_io = io.BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)
    
    return doc_io.getvalue()

def _add_bullet_content(doc, content):
    """Add content in bullet point format"""
    paragraphs = content.split('\n\n')
    for paragraph in paragraphs:
        if paragraph.strip():
            lines = paragraph.split('\n')
            for line in lines:
                if line.strip():
                    doc.add_paragraph(line.strip(), style='List Bullet')

def _add_outline_content(doc, content):
    """Add content in outline format"""
    lines = content.split('\n')
    for line in lines:
        if line.strip():
            if line.startswith('#'):
                level = line.count('#')
                doc.add_heading(line.replace('#', '').strip(), level=min(level, 3))
            else:
                doc.add_paragraph(line.strip())

def _add_qa_content(doc, content):
    """Add content in Q&A format"""
    sections = content.split('\n\n')
    for section in sections:
        if '?' in section:
            lines = section.split('\n')
            question = lines[0] if lines else section
            answer = '\n'.join(lines[1:]) if len(lines) > 1 else ""
            
            doc.add_paragraph(question, style='Heading 3')
            if answer:
                doc.add_paragraph(answer.strip())

def _add_paragraph_content(doc, content):
    """Add content in paragraph format"""
    paragraphs = content.split('\n\n')
    for paragraph in paragraphs:
        if paragraph.strip():
            doc.add_paragraph(paragraph.strip())