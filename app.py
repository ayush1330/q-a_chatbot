# app.py

import streamlit as st
from ui import show_home_page, show_resume_upload_page, show_interview_page
from agents.orchestration_agent import OrchestrationAgent
from dotenv import load_dotenv

# check test rough

load_dotenv()  # This loads the .env file at the start of your script


def main():
    st.set_page_config(page_title="AI Interviewer", page_icon=":briefcase:")

    # Initialize session state
    if "page" not in st.session_state:
        st.session_state["page"] = "home"

    # Initialize the orchestration agent and store it in session state
    if "orchestration_agent" not in st.session_state:
        # Retrieve API key from secrets
        api_key = st.secrets["openai_api_key"]
        st.session_state["orchestration_agent"] = OrchestrationAgent(api_key)

    # Navigation logic
    if st.session_state["page"] == "home":
        show_home_page()
    elif st.session_state["page"] == "upload_resume":
        show_resume_upload_page()
    elif st.session_state["page"] == "interview":
        show_interview_page()
    else:
        st.error("Unknown page")


if __name__ == "__main__":
    main()