import streamlit as st
from components.llm_selector import display_llm_selector

# Remove all _configure_* functions and display_llm_selector
# Keep only the utility functions:

def display_error_message(error_msg):
    """Display formatted error message"""
    st.error(f"❌ {error_msg}")

def display_success_message(success_msg):
    """Display formatted success message"""
    st.success(f"✅ {success_msg}")

def display_info_message(info_msg):
    """Display formatted info message"""
    st.info(f"ℹ️ {info_msg}")

def display_warning_message(warning_msg):
    """Display formatted warning message"""
    st.warning(f"⚠️ {warning_msg}")

def create_download_section(result, subject, doc_type):
    """Create download section with appropriate buttons"""
    
    st.header("💾 Download Options")
    
    if doc_type == "PowerPoint Presentation" and result.get("pptx_file"):
        st.download_button(
            label="📊 Download PowerPoint Presentation",
            data=result["pptx_file"],
            file_name=f"{subject}_{doc_type.replace(' ', '_')}.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            use_container_width=True
        )
    
    if result.get("docx_file"):
        st.download_button(
            label="📄 Download Word Document",
            data=result["docx_file"],
            file_name=f"{subject}_{doc_type.replace(' ', '_')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )