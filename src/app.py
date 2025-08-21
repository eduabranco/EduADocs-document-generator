import streamlit as st
import sys
from pathlib import Path

# Add src directory to path for imports
src_path = Path(__file__).parent
sys.path.append(str(src_path))

from components import llm_selector, document_generator
from utils.validation import validate_inputs

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
        selected_llm = llm_selector.display_llm_selector()
        
        
    
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
            placeholder="Enter the specific topic, learning objectives, or content you want to include..."
        )
        
        # Additional parameters based on document type
        if doc_type == "Exercise List":
            num_questions = st.slider("Number of Questions", 5, 50, 15)
            difficulty = st.select_slider(
                "Difficulty Level",
                options=["Easy", "Medium", "Hard", "Mixed"],
                value="Medium"
            )
            question_types = st.multiselect(
                "Question Types",
                ["Multiple Choice", "True/False", "Short Answer", "Essay", "Problem Solving"],
                default=["Multiple Choice", "Short Answer"]
            )
        
        elif doc_type == "PowerPoint Presentation":
            num_slides = st.slider("Number of Slides", 5, 30, 12)
            include_images = st.checkbox("Include image placeholders", value=True)
            presentation_style = st.selectbox(
                "Presentation Style",
                ["Educational", "Interactive", "Formal", "Creative"]
            )
        
        elif doc_type == "Summary":
            summary_length = st.selectbox(
                "Summary Length",
                ["Brief (1-2 pages)", "Detailed (3-5 pages)", "Comprehensive (5+ pages)"]
            )
            include_examples = st.checkbox("Include examples", value=True)
            format_style = st.selectbox(
                "Format Style",
                ["Bullet Points", "Paragraphs", "Outline", "Q&A Format"]
            )
    
    with col2:
        st.header("🎯 Generation Options")
        
        if st.button("🚀 Generate Document", type="primary", use_container_width=True):
            # Validate inputs
            is_valid, validation_message = validate_inputs(subject, topic, selected_llm)
            
            if is_valid:
                with st.spinner("Generating your document..."):
                    try:
                        # Prepare generation parameters
                        params = {
                            "doc_type": doc_type,
                            "subject": subject,
                            "grade_level": grade_level,
                            "topic": topic,
                            "llm_config": selected_llm
                        }
                        
                        # Add specific parameters based on document type
                        if doc_type == "Exercise List":
                            params.update({
                                "num_questions": num_questions,
                                "difficulty": difficulty,
                                "question_types": question_types
                            })
                        elif doc_type == "PowerPoint Presentation":
                            params.update({
                                "num_slides": num_slides,
                                "include_images": include_images,
                                "presentation_style": presentation_style
                            })
                        elif doc_type == "Summary":
                            params.update({
                                "summary_length": summary_length,
                                "include_examples": include_examples,
                                "format_style": format_style
                            })
                        
                        # Generate document
                        result = document_generator.generate_document(params)
                        
                        if result["success"]:
                            st.success("Document generated successfully!")
                            
                            # Display preview
                            st.header("📄 Document Preview")
                            with st.expander("View Generated Content", expanded=True):
                                st.markdown(result["content"])
                            
                            # Download options
                            st.header("💾 Download Options")
                            col_download1, col_download2 = st.columns(2)
                            
                            with col_download1:
                                if result.get("docx_file"):
                                    st.download_button(
                                        label="📄 Download Word Document",
                                        data=result["docx_file"],
                                        file_name=f"{subject}_{doc_type.replace(' ', '_')}.docx",
                                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                                    )
                            
                            with col_download2:
                                if result.get("pptx_file"):
                                    st.download_button(
                                        label="📊 Download PowerPoint",
                                        data=result["pptx_file"],
                                        file_name=f"{subject}_{doc_type.replace(' ', '_')}.pptx",
                                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                                    )
                        else:
                            st.error(f"Error generating document: {result['error']}")
                            
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
            else:
                st.warning(validation_message)
        
        # Help section
        with st.expander("❓ Help & Tips"):
            st.markdown("""
            **Getting Started:**
            1. Select your preferred AI model
            2. Choose document type and settings
            3. Describe your topic in detail
            4. Click Generate Document
            
            **For Ollama users:**
            - Make sure Ollama is running: `ollama serve`
            - Pull a model first: `ollama pull llama2`
            - Use smaller models for faster generation
            
            **Tips for better results:**
            - Be specific about learning objectives
            - Include context about student level
            - Mention any specific requirements
            - Use clear, descriptive language
            """)

if __name__ == "__main__":
    main()