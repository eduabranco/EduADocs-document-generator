# Language Selection Feature - Quick Start Guide

## 🚀 Quick Start

### For Users

1. **Run the app:**
   ```bash
   streamlit run src/app.py
   ```

2. **Switch Language:**
   - Look for the **🌐 Language / Idioma** dropdown in the sidebar
   - Select **English** or **Português**
   - The entire app interface updates instantly

3. **All content is now in your selected language:**
   - Page headers and descriptions
   - Form labels and placeholders
   - AI model configuration options
   - Help section and tips
   - Validation messages

### For Developers

#### Using Translations in Code

**Single Text Values:**
```python
from utils.language_manager import i18n

title = i18n("page.title")
label = i18n("document_settings.subject_label")
```

**Lists/Arrays:**
```python
from utils.language_manager import i18n_list

grade_levels = i18n_list("document_settings.grade_level_options")
st.selectbox("Grade Level", grade_levels)
```

**Dictionaries:**
```python
from utils.language_manager import i18n_dict

llm_config = i18n_dict("llm.openai")
```

#### Adding New Translatable Content

1. **Add to `locales/en.json`:**
   ```json
   {
     "my_feature": {
       "label": "My Label",
       "description": "My description"
     }
   }
   ```

2. **Add to `locales/pt.json`:**
   ```json
   {
     "my_feature": {
       "label": "Meu Rótulo",
       "description": "Minha descrição"
     }
   }
   ```

3. **Use in code:**
   ```python
   st.text_input(i18n("my_feature.label"), 
                 help=i18n("my_feature.description"))
   ```

## 📁 Key Files

| File | Purpose |
|------|---------|
| `src/utils/language_manager.py` | Language management logic |
| `src/components/language_selector.py` | Language selector UI |
| `locales/en.json` | English translations |
| `locales/pt.json` | Portuguese translations |

## 🌐 Supported Languages

| Language | Code | Display Name |
|----------|------|--------------|
| English | `en` | English |
| Portuguese (Brazil) | `pt` | Português |

## ✨ Features

✅ **Seamless Language Switching** - Change language without page reload
✅ **Complete Translation Coverage** - All UI text is translated
✅ **Easy to Maintain** - Centralized JSON locale files
✅ **Developer Friendly** - Simple i18n API
✅ **No Hardcoded Strings** - Consistent translation pattern
✅ **Error Handling** - Graceful fallbacks for missing translations

## 🔧 Adding a New Language

1. Create `locales/XX.json` (where XX is language code)
2. Copy structure from `locales/en.json`
3. Translate all values
4. Update `src/utils/language_manager.py`:
   ```python
   SUPPORTED_LANGUAGES = {
       "English": "en",
       "Português": "pt",
       "Español": "es"  # Add new language
   }
   ```

Done! The app automatically detects the new language.

## 📚 Translation Structure

```
Locales JSON Structure:

├── page (Page config)
├── sidebar (Sidebar elements)
├── document_settings (Form labels)
├── content_description (Content options)
├── exercise_list (Exercise parameters)
├── powerpoint (PowerPoint parameters)
├── summary (Summary parameters)
├── generation (Generation messages)
├── help (Help section)
├── llm (LLM provider configs)
│   ├── google
│   ├── openai
│   ├── ollama
│   └── huggingface
├── ui_messages (UI prefixes)
└── validation (Validation messages)
```

## 🐛 Troubleshooting

**Language doesn't change?**
- Clear browser cache
- Restart the app
- Check that both JSON files have the same keys

**Seeing missing translation error?**
- Verify key exists in both `en.json` and `pt.json`
- Check for typos in the key path
- Use `i18n()` with a `default` parameter

**Language reverts after refresh?**
- This is expected - language is session-based only
- To persist: modify language_selector.py to use browser storage

## 📖 Documentation

- **Full Documentation:** See `docs/LANGUAGE_SELECTION_FEATURE.md`
- **Implementation Details:** See `docs/LANGUAGE_SELECTION_IMPLEMENTATION.md`

## 💡 Best Practices

1. **Always use i18n functions** - Never hardcode UI strings
2. **Keep keys organized** - Use logical hierarchical keys
3. **Test both languages** - Verify translations make sense in context
4. **Use dot notation** - `section.subsection.key` format
5. **Keep translations consistent** - Same terms across sections

## 🎯 Next Steps

- [ ] Run the app with `streamlit run src/app.py`
- [ ] Test language switching in the sidebar
- [ ] Verify all UI text changes language
- [ ] Try adding a new translation string
- [ ] Consider persisting language preference if needed

---

**Need more help?** Check out the full documentation in `docs/LANGUAGE_SELECTION_FEATURE.md`
