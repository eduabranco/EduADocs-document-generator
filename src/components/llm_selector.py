import streamlit as st
import os
import requests

def display_llm_selector():
    """Display LLM selection interface and return configuration"""
    
    llm_type = st.selectbox(
        "AI Model Type",
        ["Google GenAI", "Hugging Face", "Ollama (Local)", "OpenAI API"  ],
        key="llm_type",
        index=0 # Default to Google GenAI (most capable)
    )
    
    config = {"type": llm_type}

    if llm_type == "Google GenAI":
        config.update(_configure_google())
    elif llm_type == "OpenAI API":
        config.update(_configure_openai())
    elif llm_type == "Ollama (Local)":
        config.update(_configure_ollama())
    elif llm_type == "Hugging Face":
        config.update(_configure_huggingface())
    
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
        ["gpt-5-nano", "gpt-4.1-nano", "gpt-4.1-mini", "gpt-4o-mini-search-preview"],
        index=0,  # Default to gpt-5-nano (cheaper)
        help="Choose the OpenAI model to use"
    )
    
    return {
        "api_key": api_key,
        "model": model,
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
    
    # Check if Ollama is running
    ollama_status = _check_ollama_connection(host)
    
    if ollama_status["connected"]:
        st.success(f"✅ Connected to Ollama at {host}")
        
        # Try to fetch available models
        available_models = ollama_status.get("models", [])
        
        if available_models:
            model = st.selectbox("Available Models", available_models)
        else:
            model = st.text_input(
                "Model Name",
                value="llama2",
                help="Enter the name of the Ollama model to use"
            )
            st.info("No models found. Make sure you have pulled at least one model.")
    else:
        st.error(f"❌ Cannot connect to Ollama at {host}")
        st.markdown("""
        **To fix this:**
        1. Make sure Ollama is installed
        2. Start Ollama: `ollama serve`
        3. Pull a model: `ollama pull llama2`
        4. Refresh this page
        """)
        
        model = st.text_input(
            "Model Name",
            value="llama2",
            help="Enter the name of the Ollama model to use"
        )
    
    temperature = st.slider(
        "Temperature (Creativity)",
        0.0, 1.0, 0.7
    )
    
    return {
        "host": host,
        "model": model,
        "temperature": temperature,
        "provider": "ollama",
        "connected": ollama_status["connected"]
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

def _configure_google():
    """Configure Google GenAI settings"""
    st.subheader("Google GenAI Configuration")
    
    # Try to get API key from secrets or environment
    api_key = ""
    try:
        api_key = st.secrets.get("GOOGLE_API_KEY", "")
    except:
        api_key = os.getenv("GOOGLE_API_KEY", "")
    
    if not api_key:
        api_key = st.text_input(
            "Google API Key",
            type="password",
            help="Enter your Google API key"
        )
    else:
        st.success("✅ API Key configured")
    
    model = st.selectbox(
        "Model",
        ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.5-flash-lite"],
        index=0  # Default to gemini-2.5-pro (most capable)
    )
    
    return {
        "api_key": api_key,
        "model": model,
        "provider": "google"
    }

def _check_ollama_connection(host):
    """Check if Ollama is running and get available models"""
    try:
        # Test connection with shorter timeout
        response = requests.get(f"{host}/api/tags", timeout=3)
        if response.status_code == 200:
            models_data = response.json().get("models", [])
            models = [model["name"] for model in models_data]
            return {"connected": True, "models": models}
        else:
            return {"connected": False, "error": f"HTTP {response.status_code}"}
    except requests.exceptions.ConnectionError:
        return {"connected": False, "error": "Connection refused - Ollama not running"}
    except requests.exceptions.Timeout:
        return {"connected": False, "error": "Connection timeout"}
    except Exception as e:
        return {"connected": False, "error": str(e)}
    