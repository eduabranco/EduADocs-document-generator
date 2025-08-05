from llm_handlers.api_handler import get_llm_response
from docx import Document
import io

def generate_exercises(params):
    """Generate exercise list document"""
    
    prompt = _build_exercise_prompt(params)
    
    try:
        # Get content from LLM
        content = get_llm_response(prompt, params["llm_config"])
        
        # Create Word document
        docx_file = _create_exercise_docx(content, params)
        
        return {
            "success": True,
            "content": content,
            "docx_file": docx_file
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def _build_exercise_prompt(params):
    """Build prompt for exercise generation"""
    
    prompt = f"""
    Create a comprehensive exercise list for {params['subject']} at {params['grade_level']} level.
    
    Topic: {params['topic']}
    Number of questions: {params['num_questions']}
    Difficulty: {params['difficulty']}
    Question types: {', '.join(params['question_types'])}
    
    Please structure the exercises as follows:
    1. Start with a brief introduction to the topic
    2. Organize questions by difficulty (if mixed difficulty is selected)
    3. Include clear instructions for each section
    4. For multiple choice questions, provide 4 options (A, B, C, D)
    5. For problem-solving questions, show step-by-step solutions
    6. End with an answer key
    
    Make sure the content is age-appropriate and educationally valuable.
    """
    
    return prompt

def _create_exercise_docx(content, params):
    """Create Word document from exercise content"""
    
    doc = Document()
    
    # Title
    title = doc.add_heading(f"{params['subject']} - Exercise List", 0)
    title.alignment = 1  # Center alignment
    
    # Subtitle
    doc.add_heading(f"Topic: {params['topic']}", level=2)
    doc.add_heading(f"Grade Level: {params['grade_level']}", level=3)
    
    # Add content
    paragraphs = content.split('\n\n')
    for paragraph in paragraphs:
        if paragraph.strip():
            doc.add_paragraph(paragraph.strip())
    
    # Save to bytes
    doc_io = io.BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)
    
    return doc_io.getvalue()