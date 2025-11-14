"""
Language management utility for multi-language support in the app.
Handles loading and retrieving localized text from JSON files.
"""

import json
import streamlit as st
from pathlib import Path
from typing import Dict, Any, Optional

# Path to locales folder
LOCALES_DIR = Path(__file__).parent.parent.parent / "locales"


class LanguageManager:
    """Manages language selection and localization for the app."""
    
    # Supported languages
    SUPPORTED_LANGUAGES = {
        "English": "en",
        "Português": "pt"
    }
    
    def __init__(self):
        """Initialize the language manager and load all language files."""
        self.languages = {}
        self._load_all_languages()
    
    def _load_all_languages(self) -> None:
        """Load all language JSON files from the locales directory."""
        for lang_name, lang_code in self.SUPPORTED_LANGUAGES.items():
            try:
                locale_file = LOCALES_DIR / f"{lang_code}.json"
                with open(locale_file, "r", encoding="utf-8") as f:
                    self.languages[lang_code] = json.load(f)
            except FileNotFoundError:
                print(f"Warning: Language file not found: {locale_file}")
            except json.JSONDecodeError as e:
                print(f"Warning: Error parsing language file {lang_code}.json: {e}")
    
    def get_current_language(self) -> str:
        """Get the current language code from session state."""
        if "language" not in st.session_state:
            st.session_state.language = "en"  # Default to English
        return st.session_state.language
    
    def set_language(self, lang_code: str) -> None:
        """Set the current language."""
        if lang_code in self.SUPPORTED_LANGUAGES.values():
            st.session_state.language = lang_code
        else:
            print(f"Warning: Unsupported language code: {lang_code}")
    
    def get_language_name(self, lang_code: str) -> Optional[str]:
        """Get the display name for a language code."""
        for name, code in self.SUPPORTED_LANGUAGES.items():
            if code == lang_code:
                return name
        return None
    
    def get_text(self, key_path: str, default: str = "") -> str:
        """
        Get translated text by key path (e.g., "page.title").
        
        Args:
            key_path: Dot-separated path to the text (e.g., "page.title")
            default: Default text if key is not found
            
        Returns:
            Translated text or default value
        """
        lang_code = self.get_current_language()
        lang_dict = self.languages.get(lang_code, {})
        
        keys = key_path.split(".")
        value = lang_dict
        
        try:
            for key in keys:
                value = value[key]
            return str(value)
        except (KeyError, TypeError):
            print(f"Warning: Key not found: {key_path} for language {lang_code}")
            return default
    
    def get_list(self, key_path: str, default: list = None) -> list:
        """
        Get a list of translated items by key path.
        
        Args:
            key_path: Dot-separated path to the list
            default: Default list if key is not found
            
        Returns:
            List of translated items or default value
        """
        if default is None:
            default = []
        
        try:
            lang_code = self.get_current_language()
            lang_dict = self.languages.get(lang_code, {})
            
            keys = key_path.split(".")
            value = lang_dict
            
            for key in keys:
                value = value[key]
            
            return value if isinstance(value, list) else default
        except (KeyError, TypeError):
            return default
    
    def get_dict(self, key_path: str, default: dict = None) -> dict:
        """
        Get a dictionary of translated items by key path.
        
        Args:
            key_path: Dot-separated path to the dictionary
            default: Default dictionary if key is not found
            
        Returns:
            Dictionary of translated items or default value
        """
        if default is None:
            default = {}
        
        try:
            lang_code = self.get_current_language()
            lang_dict = self.languages.get(lang_code, {})
            
            keys = key_path.split(".")
            value = lang_dict
            
            for key in keys:
                value = value[key]
            
            return value if isinstance(value, dict) else default
        except (KeyError, TypeError):
            return default


# Global instance
_language_manager = None


def get_language_manager() -> LanguageManager:
    """Get or create the global language manager instance."""
    global _language_manager
    if _language_manager is None:
        _language_manager = LanguageManager()
    return _language_manager


def i18n(key_path: str, default: str = "") -> str:
    """
    Convenience function to get translated text.
    
    Usage: i18n("page.title")
    """
    return get_language_manager().get_text(key_path, default)


def i18n_list(key_path: str, default: list = None) -> list:
    """
    Convenience function to get translated list.
    
    Usage: i18n_list("exercise_list.question_types_options")
    """
    if default is None:
        default = []
    return get_language_manager().get_list(key_path, default)


def i18n_dict(key_path: str, default: dict = None) -> dict:
    """
    Convenience function to get translated dictionary.
    
    Usage: i18n_dict("llm.openai")
    """
    if default is None:
        default = {}
    return get_language_manager().get_dict(key_path, default)
