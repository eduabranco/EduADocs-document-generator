import streamlit as st
import sys
from pathlib import Path

# Add src directory to path for imports
src_path = Path(__file__).parent
sys.path.append(str(src_path))

from components import llm_selector, document_generator, language_selector
from utils.validation import validate_inputs
from utils.language_manager import i18n, i18n_list

def main():
    st.set_page_config(
        page_title=i18n("page.title"),
        page_icon=i18n("page.icon"),
        layout="wide"
    )
    
    st.title(i18n("page.header"))
    st.markdown(i18n("page.description"))
    
    # Sidebar for LLM selection and Language selection
    with st.sidebar:
        st.header(i18n("sidebar.ai_model_selection_header"))
        selected_llm = llm_selector.display_llm_selector()
        
        # Display language selector at the bottom of sidebar
        language_selector.display_language_selector()
        
        
    
    # Main content area
    col1, col2 = st.columns([2, 1])

    
    with col1:
        st.header(i18n("document_settings.header"))
        subject = st.text_input(
            i18n("document_settings.subject_label"),
            placeholder=i18n("document_settings.subject_placeholder")
        )
        grade_level = st.selectbox(
            i18n("document_settings.grade_level_label"),
            i18n_list("document_settings.grade_level_options"),
            key="grade_level"
        )
        
        st.header(i18n("content_description.header"))
        doc_type = st.selectbox(
            i18n("content_description.document_type_label"),
            i18n_list("content_description.document_type_options"),
            key="doc_type"
        )
        topic = st.text_area(
            i18n("content_description.topic_label"),
            height=200,
            placeholder=i18n("content_description.topic_placeholder")
        )
        
        # Additional parameters based on document type
        doc_type_options = i18n_list("content_description.document_type_options")
        exercise_list_type = doc_type_options[0] if len(doc_type_options) > 0 else "Exercise List"
        powerpoint_type = doc_type_options[1] if len(doc_type_options) > 1 else "PowerPoint Presentation"
        summary_type = doc_type_options[2] if len(doc_type_options) > 2 else "Summary"
        
        if doc_type == exercise_list_type:  # Exercise List
            num_questions = st.number_input(
                i18n("exercise_list.num_questions_label"), 
                min_value=1, value=10, step=1
            )
            difficulty_options = i18n_list("exercise_list.difficulty_options")
            difficulty = st.select_slider(
                i18n("exercise_list.difficulty_label"),
                options=difficulty_options,
                value=difficulty_options[1] if len(difficulty_options) > 1 else "Medium"  # Default to Medium
            )
            question_types = st.multiselect(
                i18n("exercise_list.question_types_label"),
                i18n_list("exercise_list.question_types_options"),
                default=i18n_list("exercise_list.question_types_default")
            )
        
        elif doc_type == powerpoint_type:  # PowerPoint Presentation
            num_slides = st.number_input(
                i18n("powerpoint.num_slides_label"), 
                min_value=1, value=12, step=1
            )
            include_images = st.checkbox(
                i18n("powerpoint.include_images_label"), 
                value=True
            )
            presentation_style = st.selectbox(
                i18n("powerpoint.presentation_style_label"),
                i18n_list("powerpoint.presentation_style_options")
            )
        
        elif doc_type == summary_type:  # Summary
            summary_length = st.selectbox(
                i18n("summary.summary_length_label"),
                i18n_list("summary.summary_length_options")
            )
            include_examples = st.checkbox(
                i18n("summary.include_examples_label"), 
                value=True
            )
            format_style = st.selectbox(
                i18n("summary.format_style_label"),
                i18n_list("summary.format_style_options")
            )
    
    with col2:
        st.header(i18n("generation.options_header"))
        
        if st.button(i18n("generation.generate_button"), type="primary", use_container_width=True):
            # Validate inputs
            is_valid, validation_message = validate_inputs(subject, topic, selected_llm)
            
            if is_valid:
                with st.spinner(i18n("generation.spinner_message")):
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
                        if doc_type == exercise_list_type:
                            params.update({
                                "num_questions": num_questions,
                                "difficulty": difficulty,
                                "question_types": question_types
                            })
                        elif doc_type == powerpoint_type:
                            params.update({
                                "num_slides": num_slides,
                                "include_images": include_images,
                                "presentation_style": presentation_style
                            })
                        elif doc_type == summary_type:
                            params.update({
                                "summary_length": summary_length,
                                "include_examples": include_examples,
                                "format_style": format_style
                            })
                        
                        # Generate document
                        result = document_generator.generate_document(params)
                        
                        if result["success"]:
                            st.success(i18n("generation.success_message"))
                            
                            # Display preview
                            st.header(i18n("generation.document_preview_header"))
                            with st.expander(i18n("generation.view_generated_content"), expanded=True):
                                st.markdown(result["content"])
                            
                            # Download options
                            st.header(i18n("generation.download_options_header"))
                            col_download1, col_download2 = st.columns(2)
                            
                            with col_download1:
                                if result.get("docx_file"):
                                    st.download_button(
                                        label=i18n("generation.download_word_label"),
                                        data=result["docx_file"],
                                        file_name=f"{subject}_{doc_type.replace(' ', '_')}.docx",
                                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                                    )
                            
                            with col_download2:
                                if result.get("pptx_file"):
                                    st.download_button(
                                        label=i18n("generation.download_ppt_label"),
                                        data=result["pptx_file"],
                                        file_name=f"{subject}_{doc_type.replace(' ', '_')}.pptx",
                                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                                    )
                        else:
                            st.error(i18n("generation.error_generating_template").format(error=result['error']))
                            
                    except Exception as e:
                        st.error(i18n("generation.exception_template").format(error=str(e)))
            else:
                st.warning(validation_message)
        
        # Help section
        with st.expander(i18n("help.title")):
            getting_started = i18n_list("help.getting_started_steps")
            ollama_steps = i18n_list("help.ollama_for_users")
            tips = i18n_list("help.tips_for_better_results")
            
            st.markdown(f"""
            **Getting Started:**
            1. {getting_started[0] if len(getting_started) > 0 else ""}
            2. {getting_started[1] if len(getting_started) > 1 else ""}
            3. {getting_started[2] if len(getting_started) > 2 else ""}
            4. {getting_started[3] if len(getting_started) > 3 else ""}
            
            **For Ollama users:**
            - {ollama_steps[0] if len(ollama_steps) > 0 else ""}
            - {ollama_steps[1] if len(ollama_steps) > 1 else ""}
            - {ollama_steps[2] if len(ollama_steps) > 2 else ""}
            
            **Tips for better results:**
            - {tips[0] if len(tips) > 0 else ""}
            - {tips[1] if len(tips) > 1 else ""}
            - {tips[2] if len(tips) > 2 else ""}
            - {tips[3] if len(tips) > 3 else ""}
            """)

if __name__ == "__main__":
    main()