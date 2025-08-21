"""
Utilities Module
Common utility functions for validation and helper operations.
"""


def validate_inputs(params):
    """Validate user inputs and return list of errors"""
    errors = []
    
    # Check required fields
    if not params.get("subject", "").strip():
        errors.append("Subject is required")
    
    if not params.get("topic", "").strip():
        errors.append("Topic description is required")
    
    # Validate LLM configuration
    llm_config = params.get("llm_config", {})
    if not llm_config:
        errors.append("LLM configuration is required")
    else:
        provider = llm_config.get("provider", "")
        
        if provider == "openai_api":
            if not llm_config.get("api_key", "").strip():
                errors.append("OpenAI API key is required")
                
        elif provider == "ollama_local":
            if not llm_config.get("model", "").strip():
                errors.append("Ollama model is required")
            if not llm_config.get("host", "").strip():
                errors.append("Ollama host is required")
                
        elif provider == "hugging_face":
            if not llm_config.get("api_token", "").strip():
                errors.append("Hugging Face API token is required")
                
        else:
            errors.append("Valid LLM provider must be selected")
    
    return errors


def sanitize_filename(filename):
    """Sanitize filename for safe file creation"""
    import re
    # Remove or replace invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove multiple consecutive underscores
    sanitized = re.sub(r'_{2,}', '_', sanitized)
    # Trim underscores from start and end
    sanitized = sanitized.strip('_')
    # Ensure it's not empty
    if not sanitized:
        sanitized = "document"
    return sanitized


def format_grade_level(grade_level):
    """Format grade level for prompts"""
    grade_mappings = {
        "Elementary (K-5)": "elementary school (grades K-5)",
        "Middle School (6-8)": "middle school (grades 6-8)", 
        "High School (9-12)": "high school (grades 9-12)",
        "College/University": "college/university level",
        "Not specified": "general education"
    }
    return grade_mappings.get(grade_level, grade_level.lower())


def estimate_generation_time(doc_type, complexity_factors):
    """Estimate time for document generation"""
    base_times = {
        "Exercise List": 30,  # seconds
        "PowerPoint Presentation": 45,
        "Summary": 25
    }
    
    base_time = base_times.get(doc_type, 30)
    
    # Adjust based on complexity factors
    if "num_questions" in complexity_factors:
        base_time += complexity_factors["num_questions"] * 1.5
    if "num_slides" in complexity_factors:
        base_time += complexity_factors["num_slides"] * 2
    
    return min(base_time, 180)  # Cap at 3 minutes


def parse_topic_complexity(topic):
    """Analyze topic complexity to help with generation"""
    complexity_indicators = {
        "basic": ["introduction", "basics", "overview", "simple"],
        "intermediate": ["analyze", "compare", "explain", "discuss"],
        "advanced": ["evaluate", "synthesize", "critique", "complex"]
    }
    
    topic_lower = topic.lower()
    
    for level, indicators in complexity_indicators.items():
        if any(indicator in topic_lower for indicator in indicators):
            return level
    
    return "intermediate"  # Default to intermediate


def get_subject_keywords(subject):
    """Get subject-specific keywords for enhanced prompts"""
    subject_keywords = {
        "mathematics": ["problem-solving", "calculations", "formulas", "proofs"],
        "science": ["experiments", "observations", "hypotheses", "data analysis"],
        "history": ["chronology", "causes and effects", "primary sources", "analysis"],
        "literature": ["themes", "characters", "literary devices", "interpretation"],
        "language arts": ["grammar", "writing", "reading comprehension", "vocabulary"],
        "social studies": ["communities", "cultures", "geography", "civics"],
        "art": ["techniques", "creativity", "visual elements", "art history"],
        "music": ["rhythm", "melody", "composition", "music theory"],
        "physical education": ["fitness", "skills", "teamwork", "health"]
    }
    
    subject_lower = subject.lower()
    for key, keywords in subject_keywords.items():
        if key in subject_lower:
            return keywords
    
    return ["concepts", "understanding", "application", "practice"]


def format_content_for_display(content, max_length=1000):
    """Format content for display in Streamlit"""
    if len(content) <= max_length:
        return content
    
    # Truncate and add ellipsis
    truncated = content[:max_length]
    # Try to end at a sentence or paragraph break
    last_period = truncated.rfind('.')
    last_newline = truncated.rfind('\n')
    
    cut_point = max(last_period, last_newline)
    if cut_point > max_length * 0.8:  # If we found a good break point
        truncated = truncated[:cut_point + 1]
    
    return truncated + "\n\n... (content truncated for display)"


def get_error_message(error):
    """Get user-friendly error message"""
    error_str = str(error).lower()
    
    if "api key" in error_str or "unauthorized" in error_str:
        return "Invalid or missing API key. Please check your credentials."
    elif "timeout" in error_str:
        return "Request timed out. Please try again or check your connection."
    elif "connection" in error_str:
        return "Unable to connect to the AI service. Please check your network connection."
    elif "rate limit" in error_str:
        return "Rate limit exceeded. Please wait a moment before trying again."
    elif "model" in error_str and "not found" in error_str:
        return "The selected model is not available. Please choose a different model."
    else:
        return f"An error occurred: {error}"
