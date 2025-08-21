#!/usr/bin/env python3
"""
Teacher Document Generator - Streamlined Version
A modular Streamlit application for generating educational documents using AI.
"""

import streamlit as st
from pathlib import Path

# Import modular components
from llm_config import display_llm_selector
from document_generators import generate_document
from utils import validate_inputs

def main():
    st.set_page_config(
        page_title="Teacher Document Generator",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 Teacher Document Generator")
    st.markdown("Generate exercise lists, PowerPoint slides, and summaries for your classes")
    
    # Sidebar for LLM selection
    with st.sidebar:
        st.header("🤖 AI Model Selection")
        llm_config = display_llm_selector()
        
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📋 Document Settings")
        subject = st.text_input("Subject", placeholder="e.g., Mathematics, History, Science")
        grade_level = st.selectbox(
            "Grade Level",
            ["Elementary (K-5)", "Middle School (6-8)", "High School (9-12)", "College/University", "Not specified"],
            key="grade_level"
        )
        
        st.header("📝 Content Description")
        doc_type = st.selectbox(
            "Document Type",
            ["Exercise List", "PowerPoint Presentation", "Summary"],
            key="doc_type"
        )
        topic = st.text_area(
            "Describe the topic or provide content details:",
            height=200,
            placeholder="Provide detailed information about the topic you want to cover..."
        )
        
        # Document-specific options
        if doc_type == "Exercise List":
            num_questions = st.slider("Number of Questions", 5, 50, 15)
            difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard", "Mixed"])
            question_types = st.multiselect(
                "Question Types",
                ["Multiple Choice", "Short Answer", "Essay", "Problem Solving", "True/False"],
                default=["Multiple Choice", "Short Answer"]
            )
        elif doc_type == "PowerPoint Presentation":
            num_slides = st.slider("Number of Slides", 5, 30, 10)
            include_images = st.checkbox("Include Image Placeholders", value=True)
        else:  # Summary
            summary_length = st.selectbox("Summary Length", ["Brief", "Detailed", "Comprehensive"])
            include_examples = st.checkbox("Include Examples", value=True)
    
    with col2:
        st.header("🎯 Generation")
        
        # Validate inputs
        validation_errors = validate_inputs({
            "subject": subject,
            "topic": topic,
            "llm_config": llm_config
        })
        
        if validation_errors:
            st.error("Please fix the following issues:")
            for error in validation_errors:
                st.error(f"• {error}")
        else:
            st.success("✅ Ready to generate!")
            
            if st.button("🚀 Generate Document", type="primary", use_container_width=True):
                # Prepare parameters
                params = {
                    "subject": subject,
                    "grade_level": grade_level,
                    "topic": topic,
                    "doc_type": doc_type,
                    "llm_config": llm_config
                }
                
                # Add document-specific parameters
                if doc_type == "Exercise List":
                    params.update({
                        "num_questions": num_questions,
                        "difficulty": difficulty,
                        "question_types": question_types
                    })
                elif doc_type == "PowerPoint Presentation":
                    params.update({
                        "num_slides": num_slides,
                        "include_images": include_images
                    })
                else:  # Summary
                    params.update({
                        "summary_length": summary_length,
                        "include_examples": include_examples
                    })
                
                # Generate document
                with st.spinner(f"Generating {doc_type.lower()}..."):
                    result = generate_document(params)
                
                if result["success"]:
                    st.success("✅ Document generated successfully!")
                    
                    # Display content
                    st.subheader("Generated Content")
                    st.markdown(result["content"])
                    
                    # Provide download
                    if "file_data" in result:
                        file_ext = "docx" if doc_type in ["Exercise List", "Summary"] else "pptx"
                        st.download_button(
                            label=f"📥 Download {doc_type}",
                            data=result["file_data"],
                            file_name=f"{subject}_{doc_type.replace(' ', '_').lower()}.{file_ext}",
                            mime=f"application/vnd.openxmlformats-officedocument.{'wordprocessingml.document' if file_ext == 'docx' else 'presentationml.presentation'}"
                        )
                else:
                    st.error(f"❌ Generation failed: {result.get('error', 'Unknown error')}")

    # Footer
    st.markdown("---")
    st.markdown("**Teacher Document Generator** - Powered by AI 🤖")

if __name__ == "__main__":
    main()
