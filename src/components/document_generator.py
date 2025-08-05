from generators.exercise_generator import generate_exercises
from generators.powerpoint_generator import generate_powerpoint
from generators.summary_generator import generate_summary

def generate_document(params):
    """Main document generation coordinator"""
    
    try:
        doc_type = params["doc_type"]
        
        if doc_type == "Exercise List":
            return generate_exercises(params)
        elif doc_type == "PowerPoint Presentation":
            return generate_powerpoint(params)
        elif doc_type == "Summary":
            return generate_summary(params)
        else:
            return {"success": False, "error": "Unknown document type"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}