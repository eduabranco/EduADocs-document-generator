def validate_inputs(subject, topic, llm_config):
    """Validate user inputs before document generation"""
    
    if not subject or not subject.strip():
        return False, "Subject is required"
    
    if not topic or not topic.strip():
        return False, "Topic description is required"
    
    if not llm_config:
        return False, "AI model configuration is required"
    
    # Validate LLM configuration based on provider
    if llm_config["provider"] == "openai":
        if not llm_config.get("api_key"):
            return False, "OpenAI API key is required"
    elif llm_config["provider"] == "ollama":
        if not llm_config.get("host") or not llm_config.get("model"):
            return False, "Ollama host and model are required"
        if not llm_config.get("connected", False):
            return False, "Ollama is not connected. Please start Ollama and refresh the page"
    elif llm_config["provider"] == "huggingface":
        if not llm_config.get("model"):
            return False, "Hugging Face model is required"
    
    return True, "Valid"