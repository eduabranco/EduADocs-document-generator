# Language Selection Feature

## Overview

The EduADocs Document Generator now supports multi-language functionality. Users can switch between English and Portuguese (Português) seamlessly through the UI language selector in the sidebar.

## Architecture

### Components

#### 1. **Language Manager** (`src/utils/language_manager.py`)
The core utility that manages all language-related operations:
- Loads all language JSON files from the `locales/` directory
- Manages current language selection via Streamlit session state
- Provides convenient functions to retrieve localized text

**Key Functions:**
- `i18n(key_path, default="")` - Get translated text by dot-separated key path
  ```python
  title = i18n("page.title")  # Returns "EduADocs - Document Generator"
  ```

- `i18n_list(key_path, default=[])` - Get list of translated items
  ```python
  options = i18n_list("exercise_list.difficulty_options")
  # Returns ["Easy", "Medium", "Hard", "Mixed"]
  ```

- `i18n_dict(key_path, default={})` - Get dictionary of translated items
  ```python
  llm_config = i18n_dict("llm.openai")
  ```

#### 2. **Language Selector Component** (`src/components/language_selector.py`)
The UI component that displays language selection in the sidebar:
- Shows available languages in a dropdown
- Updates app language when selection changes
- Triggers app refresh via `st.rerun()` to apply translations

#### 3. **Locale Files** (`locales/`)
JSON files containing all translatable strings:
- `en.json` - English translations
- `pt.json` - Portuguese translations

## Supported Languages

| Language | Code | Display Name |
|----------|------|--------------|
| English | `en` | English |
| Portuguese | `pt` | Português |

## JSON Structure

The locale files are organized hierarchically for easy management:

```json
{
  "page": {
    "title": "EduADocs - Document Generator",
    "icon": "📚",
    "header": "📚 EduADocs - Document Generator",
    "description": "Generate exercise lists, PowerPoint slides, and summaries..."
  },
  "sidebar": {
    "ai_model_selection_header": "🤖 AI Model Selection",
    "ai_model_type_label": "AI Model Type",
    "ai_model_type_options": ["Google GenAI", "Hugging Face", "Ollama (Local)", "OpenAI API"]
  },
  "document_settings": {
    "header": "📋 Document Settings",
    "subject_label": "Subject",
    ...
  },
  "llm": {
    "google": { ... },
    "openai": { ... },
    "ollama": { ... },
    "huggingface": { ... }
  },
  "validation": {
    "subject_required": "Subject is required",
    ...
  }
}
```

## How to Use in Code

### In Main App (`src/app.py`)

```python
from utils.language_manager import i18n, i18n_list

# Use for single text values
st.title(i18n("page.header"))
st.text_input(i18n("document_settings.subject_label"))

# Use for lists
grade_levels = i18n_list("document_settings.grade_level_options")
st.selectbox("Grade Level", grade_levels)

# For conditional logic
doc_type = st.selectbox(
    i18n("content_description.document_type_label"),
    i18n_list("content_description.document_type_options")
)

if doc_type == i18n_list("content_description.document_type_options")[0]:  # Exercise List
    # Handle exercise list
```

### In Components

```python
from utils.language_manager import i18n, i18n_list, i18n_dict

# Get LLM configuration
llm_config = i18n_dict("llm.openai")

# Use in UI
st.subheader(i18n("llm.openai.header"))
st.text_input(i18n("llm.openai.api_key_label"))
```

### In Validation Messages

```python
from utils.language_manager import i18n

def validate_inputs(subject, topic, llm_config):
    if not subject:
        return False, i18n("validation.subject_required")
    
    if not topic:
        return False, i18n("validation.topic_required")
    
    return True, i18n("validation.valid")
```

## Adding New Languages

To add a new language (e.g., Spanish):

1. **Create new locale file**: `locales/es.json` with all translations
2. **Update Language Manager**: Add language to `SUPPORTED_LANGUAGES` dict in `src/utils/language_manager.py`:
   ```python
   SUPPORTED_LANGUAGES = {
       "English": "en",
       "Português": "pt",
       "Español": "es"  # Add this
   }
   ```
3. The app will automatically detect and load the new language

## Adding New Translatable Strings

When adding new UI text:

1. **Add key to both locale files** (`en.json` and `pt.json`):
   ```json
   {
     "new_feature": {
       "label": "English Text",
       "options": ["Option 1", "Option 2"]
     }
   }
   ```

2. **Use in code with `i18n()`**:
   ```python
   st.text_input(i18n("new_feature.label"))
   st.selectbox("Select", i18n_list("new_feature.options"))
   ```

## Session State Management

The current language is stored in Streamlit's session state:

```python
# Get current language
manager = get_language_manager()
current_lang = manager.get_current_language()  # Returns "en" or "pt"

# Set language
manager.set_language("pt")  # Switch to Portuguese

# Language changes trigger app refresh
st.rerun()  # App rerenders with new language
```

## Translation Completeness

All UI text is currently available in both English and Portuguese:
- Page configuration and headers
- Document settings and options
- LLM provider configurations (Google, OpenAI, Ollama, Hugging Face)
- Help and tips sections
- Validation messages
- Generation options
- Download labels

## Best Practices

1. **Always use i18n functions** - Never hardcode UI strings
2. **Keep translations consistent** - Use same terminology across languages
3. **Test with both languages** - Verify translations work in context
4. **Use dot notation** - Organize keys hierarchically for maintainability
5. **Handle missing keys gracefully** - Provide sensible defaults

## Troubleshooting

### Language not changing after selection
- Ensure `st.rerun()` is called in `display_language_selector()`
- Check that session state is properly initialized

### Missing translations
- Verify the key path matches exactly in both locale files
- Check for typos in key names

### Locale files not loading
- Ensure locale files are in correct directory (`locales/en.json`, `locales/pt.json`)
- Verify JSON syntax is valid using a JSON validator

## Future Enhancements

- Add more languages (Spanish, French, German, etc.)
- Persist language preference to user browser
- Add language selection to login page
- Implement automated translation validation
