import streamlit as st
import os

from components.llm_selector import _configure_google

def display_llm_selector():
    """Display LLM selection interface and return configuration"""
    
    llm_type = st.selectbox(
        "AI Model Type",
        ["OpenAI API", "Ollama (Local)", "Hugging Face"],
        key="llm_type"
    )
    
    config = {"type": llm_type}
    
    if llm_type == "OpenAI API":
        config.update(_configure_openai())
    elif llm_type == "Ollama (Local)":
        config.update(_configure_ollama())
    elif llm_type == "Hugging Face":
        config.update(_configure_huggingface())
    elif llm_type == "Google GenAI":
        config.update(_configure_google())
    
    return config

def _configure_openai():
    """Configure OpenAI API settings"""
    st.subheader("OpenAI Configuration")
    
    # Try to get API key from secrets or environment
    api_key = ""
    try:
        api_key = st.secrets.get("OPENAI_API_KEY", "")
    except:
        api_key = os.getenv("OPENAI_API_KEY", "")
    
    if not api_key:
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key"
        )
    else:
        st.success("✅ API Key configured")
    
    model = st.selectbox(
        "Model",
        ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-4o", "gpt-4o-mini"],
        index=4  # Default to gpt-4o-mini (cheaper)
    )
    
    temperature = st.slider(
        "Temperature (Creativity)",
        0.0, 1.0, 0.7,
        help="Higher values make output more creative but less focused"
    )
    
    return {
        "api_key": api_key,
        "model": model,
        "temperature": temperature,
        "provider": "openai"
    }

def _configure_ollama():
    """Configure Ollama local settings"""
    st.subheader("Ollama Configuration")
    
    host = st.text_input(
        "Ollama Host",
        value="http://localhost:11434",
        help="Ollama server URL"
    )
    
    # Try to fetch available models
    available_models = _get_ollama_models(host)
    
    if available_models:
        model = st.selectbox("Available Models", available_models)
    else:
        model = st.text_input(
            "Model Name",
            value="llama2",
            help="Enter the name of the Ollama model to use"
        )
        st.warning("Could not fetch models from Ollama. Make sure Ollama is running.")
    
    temperature = st.slider(
        "Temperature (Creativity)",
        0.0, 1.0, 0.7
    )
    
    return {
        "host": host,
        "model": model,
        "temperature": temperature,
        "provider": "ollama"
    }

def _configure_huggingface():
    """Configure Hugging Face settings"""
    st.subheader("Hugging Face Configuration")
    
    # Try to get API key from secrets or environment
    api_key = ""
    try:
        api_key = st.secrets.get("HUGGINGFACE_API_KEY", "")
    except:
        api_key = os.getenv("HUGGINGFACE_API_KEY", "")
    
    if not api_key:
        api_key = st.text_input(
            "Hugging Face API Key (Optional)",
            type="password",
            help="For private models or higher rate limits"
        )
    
    model = st.selectbox(
        "Model",
        [
            "microsoft/DialoGPT-large",
            "facebook/blenderbot-400M-distill",
            "google/flan-t5-large",
            "meta-llama/Llama-2-7b-chat-hf"
        ]
    )
    
    use_local = st.checkbox(
        "Run locally (requires model download)",
        help="Download and run model locally instead of using API"
    )
    
    temperature = st.slider(
        "Temperature (Creativity)",
        0.0, 1.0, 0.7
    )
    
    return {
        "api_key": api_key,
        "model": model,
        "use_local": use_local,
        "temperature": temperature,
        "provider": "huggingface"
    }

def _get_ollama_models(host):
    """Fetch available models from Ollama"""
    try:
        import requests
        response = requests.get(f"{host}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            return [model["name"] for model in models]
    except:
        pass
    return []

def display_error_message(error_msg):
    """Display formatted error message"""
    st.error(f"❌ {error_msg}")

def display_success_message(success_msg):
    """Display formatted success message"""
    st.success(f"✅ {success_msg}")

def display_info_message(info_msg):
    """Display formatted info message"""
    st.info(f"ℹ️ {info_msg}")

def display_warning_message(warning_msg):
    """Display formatted warning message"""
    st.warning(f"⚠️ {warning_msg}")

def create_download_section(result, subject, doc_type):
    """Create download section with appropriate buttons"""
    
    st.header("💾 Download Options")
    
    if doc_type == "PowerPoint Presentation" and result.get("pptx_file"):
        st.download_button(
            label="📊 Download PowerPoint Presentation",
            data=result["pptx_file"],
            file_name=f"{subject}_{doc_type.replace(' ', '_')}.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            use_container_width=True
        )
    
    if result.get("docx_file"):
        st.download_button(
            label="📄 Download Word Document",
            data=result["docx_file"],
            file_name=f"{subject}_{doc_type.replace(' ', '_')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )