# Teacher Document Generator - Streamlined Version

A modular Streamlit application for generating educational documents using AI. This version provides a middle ground between the full project structure and the simplified single-file version.

## Project Structure

```
teacher-doc-generator/
├── app.py                          # Main Streamlit application
├── llm_config.py                   # LLM provider configuration and API calls
├── document_generators.py          # Document generation logic
├── utils.py                        # Utility functions and validation
├── requirements_streamlined.txt    # Dependencies for this version
└── README_streamlined.md          # This file
```

## Features

- **Multiple AI Providers**: OpenAI API, Ollama (local), Hugging Face
- **Document Types**: Exercise Lists, PowerPoint Presentations, Summaries
- **File-level Modularity**: Clear separation of concerns without complex package structure
- **Validation**: Input validation and error handling
- **Download Support**: Generate and download Word/PowerPoint files

## Key Improvements

### From Full Project
- **Simplified Structure**: Removed complex package hierarchy
- **Reduced Dependencies**: Streamlined requirements
- **Single Import Path**: No nested imports or complex path management
- **Consolidated Logic**: Related functionality grouped in single files

### From Simple Version
- **Maintained Modularity**: Each concern in its own file
- **Better Organization**: Clear separation between configuration, generation, and utilities
- **Enhanced Error Handling**: Centralized validation and error management
- **Extensibility**: Easy to add new providers or document types

## Installation

1. Install dependencies:
```bash
pip install -r requirements_streamlined.txt
```

2. Set up environment variables (optional):
```bash
# For OpenAI
export OPENAI_API_KEY="your-api-key"

# For Hugging Face
export HUGGINGFACE_API_TOKEN="your-token"
```

## Usage

Run the application:
```bash
streamlit run app.py
```

## Module Overview

### `app.py`
- Main Streamlit interface
- User input handling
- UI layout and interactions
- Coordinates between modules

### `llm_config.py`
- LLM provider selection and configuration
- API key management
- Provider-specific API calls
- Connection testing (for Ollama)

### `document_generators.py`
- Document generation coordination
- Content prompting for each document type
- File creation (Word/PowerPoint)
- Content formatting and parsing

### `utils.py`
- Input validation
- Error message formatting
- Helper functions for file handling
- Content processing utilities

## Adding New Features

### New Document Type
1. Add document type to the selectbox in `app.py`
2. Add parameters collection in `app.py`
3. Implement generation function in `document_generators.py`
4. Add prompt building and file creation functions

### New AI Provider
1. Add provider option in `llm_config.py`
2. Implement configuration function
3. Add API call function
4. Update the `get_llm_response` function

### New Validation Rules
1. Add validation logic to `validate_inputs` in `utils.py`
2. Add error messages for new validation cases

## Benefits of This Structure

1. **Easy to Understand**: Each file has a clear, single responsibility
2. **Simple to Maintain**: Changes are localized to specific files
3. **Quick to Extend**: Adding features doesn't require restructuring
4. **Reduced Complexity**: No package management or complex imports
5. **Better than Monolith**: Maintains separation of concerns
6. **Deployment Friendly**: Fewer files to manage and deploy

## Migration Notes

- This version maintains all core functionality from the full project
- Configuration is streamlined but supports the same AI providers
- Document generation capabilities are preserved
- File structure is flattened for easier management
- Dependencies are reduced while maintaining essential features

## Development Tips

- Keep each module focused on its core responsibility
- Add new utilities to `utils.py` rather than creating new files
- Use type hints and docstrings for better code documentation
- Test each module independently during development
- Consider this structure for similar applications requiring modularity without complexity
