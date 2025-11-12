# EduADocs - Document Generator

This project is a Streamlit application designed to assist teachers in generating various educational documents, including exercise lists, PowerPoint slides, and summaries. The application allows users to select their preferred language model (LLM) from APIs, Ollama, or Hugging Face for document generation.

## Features

- **Exercise List Generation**: Create customized exercise lists based on specified subjects and requirements.
- **PowerPoint Slide Creation**: Generate PowerPoint presentations with content tailored to user specifications.
- **Summary Generation**: Summarize provided content effectively for quick reference.
- **LLM Selection**: Choose from multiple LLMs to suit different document generation needs.

## Project Structure

```
EduADocs-doc-generator
├── src
│   ├── app.py
│   ├── components
│   │   ├── document_generator.py
│   │   ├── llm_selector.py
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
│       ├── file_utils.py
│       └── validation.py
├── config
│   └── settings.py
├── templates
│   ├── exercise_template.py
│   ├── powerpoint_template.py
│   └── summary_template.py
├── requirements.txt
├── .streamlit
│   └── config.toml
├── .gitignore
└── README.md
```

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

## Documentation

Additional technical documentation and implementation notes can be found in the [`docs/`](./docs/) directory:

- **[PowerPoint Generator Fix](./docs/POWERPOINT_FIX_SUMMARY.md)** - Details about PowerPoint generation improvements
- **[Ollama Cleanup Fix](./docs/OLLAMA_CLEANUP_FIX.md)** - Implementation of thinking tags cleanup
- **[All Documentation Index](./docs/README.md)** - Complete documentation index

## Project Variants

This project has multiple variants available:

- **[Simplified Version](./simplified/)** - Minimal implementation with basic features
- **[Streamlined Version](./streamlined/)** - Optimized version with enhanced performance

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
