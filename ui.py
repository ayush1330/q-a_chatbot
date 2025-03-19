# ui.py

import streamlit as st
from utils.file_utils import save_uploaded_file, validate_file_type, is_file_size_valid, extract_text_from_resume


def show_home_page():
    st.title("Welcome to AI Interviewer")
    st.write("I'm here to guide you through your interview process.")
    if st.button("Start Your Interview"):
        st.session_state["page"] = "upload_resume"


def show_resume_upload_page():
    st.header("Upload Your Resume")
    st.write("Please upload your resume in PDF or DOCX format. Maximum size: 5MB.")

    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    allowed_types = [".pdf", ".docx"]

    # Initialize session state variables
    if "resume_uploaded" not in st.session_state:
        st.session_state["resume_uploaded"] = False
    if "resume_saved" not in st.session_state:
        st.session_state["resume_saved"] = False
    if "interview_started" not in st.session_state:
        st.session_state["interview_started"] = False

    if not st.session_state["resume_uploaded"]:
        uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx"])

        if uploaded_file is not None:
            if not validate_file_type(uploaded_file, allowed_types):
                st.error("Unsupported file type. Please upload a PDF or DOCX file.")
            elif not is_file_size_valid(uploaded_file, MAX_FILE_SIZE):
                st.error(
                    "File size exceeds the 5MB limit. Please upload a smaller file."
                )
            else:
                # Save the uploaded file
                file_path = save_uploaded_file(uploaded_file)
                st.session_state["resume_uploaded"] = True
                st.session_state["resume_saved"] = True
                st.success("Thank you! Your resume has been successfully uploaded.")
                
                # Extract text from the resume
                resume_text = extract_text_from_resume(file_path)
                # Load the resume text into the orchestration agent
                st.session_state["orchestration_agent"].load_resume(resume_text)

                # Render the "Start Interview" button
                if st.button("Start Interview"):
                    st.session_state["interview_started"] = True
                    st.session_state["page"] = "interview"
    else:
        st.warning("You have already uploaded your resume.")
        if not st.session_state["interview_started"]:
            # Render the "Start Interview" button
            if st.button("Start Interview"):
                st.session_state["interview_started"] = True
                st.session_state["page"] = "interview"
        else:
            st.write("Interview will start shortly...")


def show_interview_page():
    st.header("Interview")
    # Access orchestration_agent from st.session_state
    orchestration_agent = st.session_state["orchestration_agent"]
    orchestration_agent.start_interview()
