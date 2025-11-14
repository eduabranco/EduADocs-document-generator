import os
import requests
import json
import time
import re

def _clean_thinking_tags(text):
    """Remove <think> and </think> tags and content between them from text"""
    if not text:
        return text
    
    # Remove thinking tags and their content (case-insensitive, multiline)
    pattern = r'<think>.*?</think>'
    cleaned_text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.DOTALL)
    
    # Also handle self-closing think tags
    pattern_self_closing = r'<think\s*/>'
    cleaned_text = re.sub(pattern_self_closing, '', cleaned_text, flags=re.IGNORECASE)
    
    # Clean up extra whitespace that might be left behind
    # Replace multiple consecutive newlines with just two newlines
    cleaned_text = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned_text)
    
    # Remove leading/trailing whitespace from each line while preserving structure
    lines = cleaned_text.split('\n')
    cleaned_lines = []
    for line in lines:
        cleaned_lines.append(line.rstrip())
    
    cleaned_text = '\n'.join(cleaned_lines)
    cleaned_text = cleaned_text.strip()
    
    return cleaned_text

def get_llm_response(prompt, llm_config):
    """Get response from configured LLM"""
    
    provider = llm_config["provider"]
    
    if provider == "openai":
        return _get_openai_response(prompt, llm_config)
    elif provider == "ollama":
        return _get_ollama_response(prompt, llm_config)
    elif provider == "huggingface":
        return _get_huggingface_response(prompt, llm_config)
    elif provider == "google":
        return _get_google_response(prompt, llm_config)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

def _get_openai_response(prompt, config):
    """Get response from OpenAI API"""
    
    if not config.get("api_key"):
        raise ValueError("OpenAI API key is required")
    
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": config["model"],
        "messages": [{"role": "user", "content": prompt}],
    }
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code != 200:
            error_msg = f"OpenAI API error: {response.status_code}"
            try:
                error_detail = response.json().get("error", {}).get("message", "")
                if error_detail:
                    error_msg += f" - {error_detail}"
            except:
                pass
            raise Exception(error_msg)
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
        
    except requests.exceptions.Timeout:
        raise Exception("OpenAI API timeout. Please try again.")
    except requests.exceptions.ConnectionError:
        raise Exception("Cannot connect to OpenAI API. Check your internet connection.")
    except Exception as e:
        if "API error" in str(e):
            raise e
        else:
            raise Exception(f"OpenAI API error: {str(e)}")

def _get_ollama_response(prompt, config):
    """Get response from Ollama local instance"""
    
    # Check if connection was verified during configuration
    if not config.get("connected", False):
        raise Exception("Ollama is not running or not accessible. Please start Ollama and try again.")
    
    data = {
        "model": config["model"],
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": config["temperature"]
        }
    }
    
    try:
        # First, check if the model exists
        models_response = requests.get(f"{config['host']}/api/tags", timeout=5)
        if models_response.status_code == 200:
            available_models = [m["name"] for m in models_response.json().get("models", [])]
            if config["model"] not in available_models:
                raise Exception(f"Model '{config['model']}' not found. Available models: {', '.join(available_models)}")
        
        # Generate response with longer timeout for generation
        response = requests.post(
            f"{config['host']}/api/generate",
            json=data,
            timeout=300  # 5 minutes timeout for generation
        )
        
        if response.status_code != 200:
            raise Exception(f"Ollama API error: {response.status_code} - {response.text}")
        
        result = response.json()
        raw_response = result.get("response", "No response generated")
        
        # Clean thinking tags from Ollama response
        cleaned_response = _clean_thinking_tags(raw_response)
        
        return cleaned_response
        
    except requests.exceptions.Timeout:
        raise Exception("Ollama generation timeout. The model might be too slow or the prompt too complex. Try a simpler prompt or a faster model.")
    except requests.exceptions.ConnectionError:
        raise Exception("Cannot connect to Ollama. Make sure Ollama is running with 'ollama serve'.")
    except Exception as e:
        if "API error" in str(e) or "not found" in str(e) or "timeout" in str(e):
            raise e
        else:
            raise Exception(f"Ollama error: {str(e)}")

def _get_huggingface_response(prompt, config):
    """Get response from Hugging Face"""
    
    if config["use_local"]:
        return _get_huggingface_local_response(prompt, config)
    else:
        return _get_huggingface_api_response(prompt, config)

def _get_huggingface_api_response(prompt, config):
    """Get response from Hugging Face API"""
    
    headers = {"Content-Type": "application/json"}
    if config.get("api_key"):
        headers["Authorization"] = f"Bearer {config['api_key']}"
    
    data = {
        "inputs": prompt,
        "parameters": {
            "temperature": config["temperature"],
            "max_new_tokens": 2000,
            "return_full_text": False
        }
    }
    
    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{config['model']}",
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code == 503:
            # Model is loading
            raise Exception("Model is loading on Hugging Face. Please wait a moment and try again.")
        elif response.status_code != 200:
            raise Exception(f"Hugging Face API error: {response.status_code} - {response.text}")
        
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            if isinstance(result[0], dict):
                return result[0].get("generated_text", str(result[0]))
            else:
                return str(result[0])
        elif isinstance(result, dict):
            return result.get("generated_text", str(result))
        else:
            return str(result)
            
    except requests.exceptions.Timeout:
        raise Exception("Hugging Face API timeout. Please try again.")
    except requests.exceptions.ConnectionError:
        raise Exception("Cannot connect to Hugging Face API. Check your internet connection.")
    except Exception as e:
        if "API error" in str(e) or "loading" in str(e):
            raise e
        else:
            raise Exception(f"Hugging Face error: {str(e)}")

def _get_huggingface_local_response(prompt, config):
    """Get response from local Hugging Face model"""
    
    try:
        from transformers import pipeline
        
        # This is a simplified implementation
        # In production, you'd want to cache the model loading
        generator = pipeline(
            "text-generation",
            model=config["model"],
            temperature=config["temperature"]
        )
        
        result = generator(prompt, max_length=2000, num_return_sequences=1)
        return result[0]["generated_text"]
        
    except ImportError:
        raise Exception("transformers library not installed for local Hugging Face models. Install with: pip install transformers torch")
    except Exception as e:
        raise Exception(f"Local Hugging Face model error: {str(e)}")
    
def _get_google_response(prompt, config):
    """Get response from Google GenAI API"""
    
    if not config.get("api_key"):
        raise ValueError("Google API key is required")

    try:
        import google.genai as genai
        os.environ["GOOGLE_API_KEY"] = config["api_key"]
        client=genai.Client()
        response = client.models.generate_content(model=config["model"], contents=prompt)
        
        return response.text
    except Exception as e:
        raise Exception(f"Google GenAI API error: {str(e)}")
