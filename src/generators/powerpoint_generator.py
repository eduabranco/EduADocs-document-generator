from llm_handlers.api_handler import get_llm_response
from pptx import Presentation
from pptx.util import Inches
import io

def generate_powerpoint(params):
    """Generate PowerPoint presentation"""
    
    prompt = _build_powerpoint_prompt(params)
    
    try:
        # Get content from LLM
        content = get_llm_response(prompt, params["llm_config"])
        
        # Create PowerPoint file
        pptx_file = _create_powerpoint_pptx(content, params)
        
        return {
            "success": True,
            "content": content,
            "pptx_file": pptx_file
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def _build_powerpoint_prompt(params):
    """Build prompt for PowerPoint generation"""
    
    prompt = f"""
    Create a {params['num_slides']}-slide PowerPoint presentation outline for {params['subject']} at {params['grade_level']} level.
    
    Topic: {params['topic']}
    Presentation style: {params['presentation_style']}
    Include images: {params['include_images']}
    
    For each slide, provide:
    1. Slide title
    2. Main bullet points (3-5 per slide)
    3. Speaker notes
    {'4. Image suggestions (if applicable)' if params['include_images'] else ''}
    
    Format your response as:
    SLIDE 1: [Title]
    - Bullet point 1
    - Bullet point 2
    - Bullet point 3
    NOTES: [Speaker notes for this slide]
    {'IMAGE: [Image description/suggestion]' if params['include_images'] else ''}
    
    Make the presentation engaging and educational for the target grade level.
    """
    
    return prompt

def _create_powerpoint_pptx(content, params):
    """Create PowerPoint file from content"""
    
    prs = Presentation()
    
    # Parse content and create slides
    slides_data = _parse_powerpoint_content(content)
    
    for slide_data in slides_data:
        slide_layout = prs.slide_layouts[1]  # Title and Content layout
        slide = prs.slides.add_slide(slide_layout)
        
        # Title
        title = slide.shapes.title
        title.text = slide_data.get('title', 'Slide Title')
        
        # Content
        content_placeholder = slide.placeholders[1]
        text_frame = content_placeholder.text_frame
        text_frame.text = slide_data.get('bullets', ['No content'])[0]
        
        # Add bullet points
        for bullet in slide_data.get('bullets', [])[1:]:
            p = text_frame.add_paragraph()
            p.text = bullet
            p.level = 0
        
        # Add notes
        if slide_data.get('notes'):
            notes_slide = slide.notes_slide
            notes_text_frame = notes_slide.notes_text_frame
            notes_text_frame.text = slide_data['notes']
    
    # Save to bytes
    pptx_io = io.BytesIO()
    prs.save(pptx_io)
    pptx_io.seek(0)
    
    return pptx_io.getvalue()

def _parse_powerpoint_content(content):
    """Parse LLM response into slide data"""
    
    slides = []
    current_slide = {}
    
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        if line.startswith('SLIDE'):
            if current_slide:
                slides.append(current_slide)
            current_slide = {
                'title': line.split(':', 1)[1].strip() if ':' in line else 'Slide',
                'bullets': [],
                'notes': '',
                'image': ''
            }
        elif line.startswith('- '):
            if current_slide:
                current_slide['bullets'].append(line[2:])
        elif line.startswith('NOTES:'):
            if current_slide:
                current_slide['notes'] = line[6:].strip()
        elif line.startswith('IMAGE:'):
            if current_slide:
                current_slide['image'] = line[6:].strip()
    
    if current_slide:
        slides.append(current_slide)
    
    return slides