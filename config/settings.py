import os

class Settings:
    def __init__(self):
        self.llm_api_key = os.getenv("LLM_API_KEY", "<your_api_key>")
        self.llm_model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
        self.output_directory = os.getenv("OUTPUT_DIRECTORY", "./generated_docs")
        self.allowed_file_types = ["pdf", "pptx", "txt"]
        self.streamlit_port = int(os.getenv("STREAMLIT_PORT", 8501))
        self.debug_mode = os.getenv("DEBUG_MODE", "False").lower() in ("true", "1", "t")