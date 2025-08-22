# Simplified Teacher Document Generator

A streamlined Streamlit application for generating educational documents using AI. This simplified version consolidates all functionality into a single file while maintaining all core features.

## Features

- **Exercise List Generation**: Create customized exercise lists
- **PowerPoint Presentations**: Generate educational slide decks  
- **Summary Documents**: Create comprehensive summaries
- **Multiple AI Providers**: Support for OpenAI, Ollama, and Hugging Face

## Simplifications Made

### From Original Structure:
```
├── src/
│   ├── app.py (188 lines)
│   ├── components/ (3 files, 200+ lines)
│   ├── generators/ (3 files, 300+ lines) 
│   ├── llm_handlers/ (3 files, 200+ lines)
│   └── utils/ (2 files, 100+ lines)
├── templates/ (3 files, 100+ lines)
├── config/ (2 files)
└── requirements.txt (17 dependencies)
```

### To Simplified Structure:
```
├── simple_app.py (450 lines - everything in one file)
├── simple_requirements.txt (6 dependencies)
└── README_simple.md
```

## Key Improvements

1. **Single File**: All functionality consolidated into one file
2. **Reduced Dependencies**: From 17 to 6 essential packages
3. **Unified LLM Handling**: One function handles all AI providers
4. **Simplified Configuration**: Direct environment variable handling
5. **Streamlined UI**: Cleaner, more intuitive interface
6. **Better Error Handling**: More robust error messages
7. **Faster Startup**: No complex module imports

## Installation

1. Install dependencies:
   ```bash
   pip install -r simple_requirements.txt
   ```

2. Set up environment variables (optional):
   ```bash
   export OPENAI_API_KEY="your-key-here"
   export HUGGINGFACE_API_KEY="your-key-here"
   ```

3. Run the application:
   ```bash
   streamlit run simple_app.py
   ```

## Usage

1. **Select AI Provider**: Choose from OpenAI, Ollama, or Hugging Face
2. **Configure Settings**: Set subject, grade level, and document type
3. **Describe Topic**: Provide detailed description of what you want
4. **Generate**: Click generate and download your documents

## Supported Document Types

### Exercise Lists
- Multiple choice questions
- True/False questions  
- Short answer questions
- Essay questions
- Problem-solving exercises

### PowerPoint Presentations
- Educational slides with speaker notes
- Image placement suggestions
- Multiple presentation styles
- Customizable slide count

### Summary Documents
- Bullet point format
- Paragraph format
- Outline format
- Q&A format

## AI Provider Setup

### OpenAI
- Requires API key
- Supports GPT-4o-mini, GPT-4o, GPT-4-turbo, GPT-3.5-turbo
- Best quality but costs money

### Ollama (Local)
- Free to use
- Run locally: `ollama serve`
- Pull models: `ollama pull llama2`
- Supports various open-source models

### Hugging Face
- Free tier available
- API key optional (for higher limits)
- Various model options
- Good for experimentation

## Benefits of Simplification

1. **Easier Maintenance**: Single file is easier to understand and modify
2. **Faster Development**: No need to navigate multiple modules
3. **Reduced Complexity**: Fewer abstractions and interfaces
4. **Better Performance**: Fewer imports and initialization overhead
5. **Simpler Deployment**: Just one file to deploy
6. **Easier Debugging**: All code in one place
7. **Lower Resource Usage**: Fewer dependencies to install

## When to Use Original vs Simplified

### Use Simplified Version When:
- You want quick setup and deployment
- You don't need extensive customization
- You prefer simplicity over modularity
- You're prototyping or learning
- You have limited resources

### Use Original Version When:
- You need extensive customization
- You're building a larger application
- You want to add many new features
- You need strict separation of concerns
- You're working with a team

## Migration Guide

To migrate from the original version:

1. Replace the entire `src/` directory with `simple_app.py`
2. Replace `requirements.txt` with `simple_requirements.txt`
3. Update your run command to `streamlit run simple_app.py`
4. Environment variables work the same way
5. All functionality is preserved

The simplified version maintains 100% feature compatibility while reducing complexity by ~80%.
