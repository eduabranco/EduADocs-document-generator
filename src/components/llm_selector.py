import streamlit as st
import os
import requests
from utils.language_manager import i18n, i18n_list, i18n_dict

def display_llm_selector():
    """Display LLM selection interface and return configuration"""
    
    llm_options = i18n_list("sidebar.ai_model_type_options")
    
    llm_type = st.selectbox(
        i18n("sidebar.ai_model_type_label"),
        llm_options,
        key="llm_type",
        index=0  # Default to Google GenAI (most capable)
    )
    
    config = {"type": llm_type}

    # Compare with actual strings from the list
    google_llm = llm_options[0] if len(llm_options) > 0 else "Google GenAI"
    huggingface_llm = llm_options[1] if len(llm_options) > 1 else "Hugging Face"
    ollama_llm = llm_options[2] if len(llm_options) > 2 else "Ollama (Local)"
    openai_llm = llm_options[3] if len(llm_options) > 3 else "OpenAI API"
    
    if llm_type == google_llm:  # Google GenAI
        config.update(_configure_google())
    elif llm_type == openai_llm:  # OpenAI API
        config.update(_configure_openai())
    elif llm_type == ollama_llm:  # Ollama (Local)
        config.update(_configure_ollama())
    elif llm_type == huggingface_llm:  # Hugging Face
        config.update(_configure_huggingface())
    
    return config

def _configure_openai():
    """Configure OpenAI API settings"""
    st.subheader(i18n("llm.openai.header"))
    
    # Try to get API key from secrets or environment
    api_key = ""
    try:
        api_key = st.secrets.get("OPENAI_API_KEY", "")
    except:
        api_key = os.getenv("OPENAI_API_KEY", "")
    
    if not api_key:
        api_key = st.text_input(
            i18n("llm.openai.api_key_label"),
            type="password",
            help=i18n("llm.openai.api_key_help")
        )
    else:
        st.success(i18n("llm.openai.api_key_configured"))
    
    model = st.selectbox(
        i18n("llm.openai.model_label"),
        i18n_list("llm.openai.model_options"),
        index=0,  # Default to gpt-5-nano (cheaper)
        help=i18n("llm.openai.model_help")
    )
    
    return {
        "api_key": api_key,
        "model": model,
        "provider": "openai"
    }

def _configure_ollama():
    """Configure Ollama local settings"""
    st.subheader(i18n("llm.ollama.header"))
    
    host = st.text_input(
        i18n("llm.ollama.host_label"),
        value="http://localhost:11434",
        help=i18n("llm.ollama.host_help")
    )
    
    # Check if Ollama is running
    ollama_status = _check_ollama_connection(host)
    
    if ollama_status["connected"]:
        st.success(i18n("llm.ollama.connected_template").format(host=host))
        
        # Try to fetch available models
        available_models = ollama_status.get("models", [])
        
        if available_models:
            model = st.selectbox(i18n("sidebar.ai_model_type_label"), available_models)
        else:
            model = st.text_input(
                i18n("llm.ollama.model_name_label"),
                value="llama2",
                help=i18n("llm.ollama.model_name_help")
            )
            st.info(i18n("llm.ollama.no_models_info"))
    else:
        st.error(i18n("llm.ollama.cannot_connect_template").format(host=host))
        
        fix_steps = i18n_list("llm.ollama.fix_steps")
        st.markdown(f"""
        **To fix this:**
        1. {fix_steps[0] if len(fix_steps) > 0 else ""}
        2. {fix_steps[1] if len(fix_steps) > 1 else ""}
        3. {fix_steps[2] if len(fix_steps) > 2 else ""}
        4. {fix_steps[3] if len(fix_steps) > 3 else ""}
        """)
        
        model = st.text_input(
            i18n("llm.ollama.model_name_label"),
            value="llama2",
            help=i18n("llm.ollama.model_name_help")
        )
    
    temperature = st.slider(
        i18n("llm.ollama.temperature_label"),
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
    st.subheader(i18n("llm.huggingface.header"))
    
    # Try to get API key from secrets or environment
    api_key = ""
    try:
        api_key = st.secrets.get("HUGGINGFACE_API_KEY", "")
    except:
        api_key = os.getenv("HUGGINGFACE_API_KEY", "")
    
    if not api_key:
        api_key = st.text_input(
            i18n("llm.huggingface.api_key_label"),
            type="password",
            help=i18n("llm.huggingface.api_key_help")
        )
    
    model = st.selectbox(
        i18n("llm.huggingface.model_label"),
        i18n_list("llm.huggingface.model_options")
    )
    
    use_local = st.checkbox(
        i18n("llm.huggingface.run_locally_label"),
        help=i18n("llm.huggingface.run_locally_help")
    )
    
    temperature = st.slider(
        i18n("llm.huggingface.temperature_label"),
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
    st.subheader(i18n("llm.google.header"))
    
    # Try to get API key from secrets or environment
    api_key = ""
    try:
        api_key = st.secrets.get("GOOGLE_API_KEY", "")
    except:
        api_key = os.getenv("GOOGLE_API_KEY", "")
    
    if not api_key:
        api_key = st.text_input(
            i18n("llm.google.api_key_label"),
            type="password",
            help=i18n("llm.google.api_key_help")
        )
    else:
        st.success(i18n("llm.google.api_key_configured"))
    
    model = st.selectbox(
        i18n("llm.google.model_label"),
        i18n_list("llm.google.model_options"),
        index=0,  # Default to gemini-2.5-pro (most capable)
        help=i18n("llm.google.model_help")
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
    