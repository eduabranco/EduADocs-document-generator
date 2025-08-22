"""
LLM Configuration Module
Handles the selection and configuration of different AI model providers.
"""

import streamlit as st
import os
import requests


def display_llm_selector():
    """Display LLM selection interface and return configuration"""
    
    llm_type = st.selectbox(
        "AI Model Type",
        ["OpenAI API", "Ollama (Local)", "Hugging Face"],
        key="llm_type"
    )
    
    config = {"provider": llm_type.lower().replace(" ", "_").replace("(", "").replace(")", "")}
    
    if llm_type == "OpenAI API":
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
        ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
        index=0  # Default to gpt-4o-mini (cheaper)
    )
    
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Controls randomness in output. Higher values = more creative"
    )
    
    return {
        "api_key": api_key,
        "model": model,
        "temperature": temperature
    }


def _configure_ollama():
    """Configure Ollama local API settings"""
    st.subheader("Ollama Configuration")
    
    host = st.text_input(
        "Ollama Host",
        value="http://localhost:11434",
        help="URL where Ollama is running"
    )
    
    # Check if Ollama is available
    is_available, available_models = _check_ollama_connection(host)
    
    if is_available:
        st.success(f"✅ Connected to Ollama ({len(available_models)} models found)")
        
        if available_models:
            model = st.selectbox("Model", available_models)
        else:
            model = st.text_input("Model Name", value="llama2")
            st.warning("⚠️ No models found. Make sure to pull models first.")
    else:
        st.error("❌ Cannot connect to Ollama. Make sure it's running.")
        model = st.selectbox(
            "Model", 
            ["llama2", "mistral", "codellama", "phi", "neural-chat"],
            help="Select a model (connection will be attempted during generation)"
        )
    
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1
    )
    
    return {
        "host": host,
        "model": model,
        "temperature": temperature,
        "available": is_available
    }


def _configure_huggingface():
    """Configure Hugging Face API settings"""
    st.subheader("Hugging Face Configuration")
    
    # Get API token
    api_token = ""
    try:
        api_token = st.secrets.get("HUGGINGFACE_API_TOKEN", "")
    except:
        api_token = os.getenv("HUGGINGFACE_API_TOKEN", "")
    
    if not api_token:
        api_token = st.text_input(
            "Hugging Face API Token",
            type="password",
            help="Enter your Hugging Face API token"
        )
    else:
        st.success("✅ API Token configured")
    
    model = st.selectbox(
        "Model",
        [
            "microsoft/DialoGPT-large",
            "google/flan-t5-large", 
            "facebook/blenderbot-400M-distill",
            "microsoft/DialoGPT-medium"
        ]
    )
    
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )
    
    return {
        "api_token": api_token,
        "model": model,
        "temperature": temperature
    }


def _check_ollama_connection(host="http://localhost:11434"):
    """Check if Ollama is running and get available models"""
    try:
        response = requests.get(f"{host}/api/tags", timeout=3)
        if response.status_code == 200:
            models = [m["name"] for m in response.json().get("models", [])]
            return True, models
        return False, []
    except Exception:
        return False, []


def get_llm_response(prompt, config):
    """Unified function to get LLM response based on provider"""
    provider = config["provider"]
    
    if provider == "openai_api":
        return _call_openai(prompt, config)
    elif provider == "ollama_local":
        return _call_ollama(prompt, config)
    elif provider == "hugging_face":
        return _call_huggingface(prompt, config)
    else:
        raise ValueError(f"Unsupported provider: {provider}")


def _call_openai(prompt, config):
    """Call OpenAI API"""
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": config["model"],
        "messages": [{"role": "user", "content": prompt}],
        "temperature": config.get("temperature", 0.7),
        "max_tokens": 4000
    }
    
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=data,
        timeout=60
    )
    
    if response.status_code != 200:
        raise Exception(f"OpenAI API error: {response.status_code} - {response.text}")
    
    result = response.json()
    return result["choices"][0]["message"]["content"]


def _call_ollama(prompt, config):
    """Call Ollama local API"""
    data = {
        "model": config["model"],
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": config.get("temperature", 0.7)}
    }
    
    response = requests.post(
        f"{config['host']}/api/generate",
        json=data,
        timeout=300
    )
    
    if response.status_code != 200:
        raise Exception(f"Ollama API error: {response.status_code}")
    
    result = response.json()
    return result["response"]


def _call_huggingface(prompt, config):
    """Call Hugging Face API"""
    headers = {
        "Authorization": f"Bearer {config['api_token']}",
        "Content-Type": "application/json"
    }
    
    data = {
        "inputs": prompt,
        "parameters": {
            "temperature": config.get("temperature", 0.7),
            "max_length": 1000
        }
    }
    
    response = requests.post(
        f"https://api-inference.huggingface.co/models/{config['model']}",
        headers=headers,
        json=data,
        timeout=60
    )
    
    if response.status_code != 200:
        raise Exception(f"Hugging Face API error: {response.status_code}")
    
    result = response.json()
    if isinstance(result, list) and len(result) > 0:
        return result[0].get("generated_text", "No response generated")
    else:
        return str(result)
