"""
Language selector UI component.
Displays language selection in the sidebar.
"""

import streamlit as st
from utils.language_manager import get_language_manager


def display_language_selector() -> None:
    """
    Display language selector in the sidebar.
    Allows users to switch between available languages.
    """
    lang_manager = get_language_manager()
    current_lang = lang_manager.get_current_language()
    
    # Get language display name
    lang_display_names = list(lang_manager.SUPPORTED_LANGUAGES.keys())
    lang_codes = list(lang_manager.SUPPORTED_LANGUAGES.values())
    
    current_lang_index = lang_codes.index(current_lang) if current_lang in lang_codes else 0
    
    st.markdown("---")
    st.subheader("🌐 Language / Idioma")
    
    selected_lang_name = st.selectbox(
        "Select Language",
        lang_display_names,
        index=current_lang_index,
        key="language_selector",
        label_visibility="collapsed"
    )
    
    # Get the language code for the selected language name
    selected_lang_code = lang_manager.SUPPORTED_LANGUAGES[selected_lang_name]
    
    # Update language if changed
    if selected_lang_code != current_lang:
        lang_manager.set_language(selected_lang_code)
        st.rerun()
