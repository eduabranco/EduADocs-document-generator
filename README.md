# EduADocs - Document Generator

This project is a Streamlit application designed to assist teachers in generating various educational documents, including exercise lists, PowerPoint slides, and summaries. The application allows users to select their preferred language model (LLM) from APIs, Ollama, or Hugging Face for document generation.

## Features

- **Multi-Language Support**: Choose between English and Portuguese (Português) 🌐
- **Exercise List Generation**: Create customized exercise lists based on specified subjects and requirements.
- **PowerPoint Slide Creation**: Generate PowerPoint presentations with content tailored to user specifications.
- **Summary Generation**: Summarize provided content effectively for quick reference.
- **LLM Selection**: Choose from multiple LLMs (Google GenAI, OpenAI, Ollama, Hugging Face) to suit different document generation needs.

## Project Structure

```
EduADocs-doc-generator
├── src
│   ├── app.py
│   ├── components
│   │   ├── document_generator.py
│   │   ├── llm_selector.py
│   │   ├── language_selector.py
│   │   └── ui_components.py
│   ├── generators
│   │   ├── exercise_generator.py
│   │   ├── powerpoint_generator.py
│   │   └── summary_generator.py
│   ├── llm_handlers
│   │   ├── api_handler.py
│   │   ├── ollama_handler.py
│   │   └── huggingface_handler.py
│   └── utils
│       ├── language_manager.py
│       ├── file_utils.py
│       └── validation.py
├── locales
│   ├── en.json
│   └── pt.json
├── requirements.txt
├── .streamlit
│   └── config.toml
├── .gitignore
└── README.md
```

## 🌐 Language Support

The application supports multiple languages for a global audience:

- **English** (en) - Default language
- **Português** (pt) - Brazilian Portuguese

You can easily switch between languages using the language selector in the sidebar without refreshing the page.

### Adding New Languages

To add a new language:

1. Create a new JSON file in the `locales/` directory (e.g., `locales/es.json`)
2. Copy the structure from `locales/en.json` and translate all strings
3. Update `src/utils/language_manager.py` to include the new language in `SUPPORTED_LANGUAGES`

For detailed instructions, see [LANGUAGE_QUICKSTART.md](LANGUAGE_QUICKSTART.md)

## Installation

1. Clone the repository:

   ```
   git clone <repository-url>
   cd EduADocs-doc-generator
   ```
2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```
3. Set up your environment variables for API keys and other configurations as needed in `config/settings.py`.

## Usage

To run the application, execute the following command:

```
streamlit run src/app.py
```

Open your web browser and navigate to `http://localhost:8501` to access the application.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
