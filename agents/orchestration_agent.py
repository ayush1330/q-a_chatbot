# agents/orchestration_agent.py

import streamlit as st
from langchain.memory import ConversationBufferMemory
from agents.question_generation_agent import QuestionGenerationAgent


class OrchestrationAgent:
    def __init__(self, api_key):
        # Initialize conversation memory
        self.memory = ConversationBufferMemory()

        # Initialize the QuestionGenerationAgent
        self.question_agent = QuestionGenerationAgent(api_key)

        # Placeholder for resume text
        self.resume_text = ""

    def load_resume(self, resume_text):
        self.resume_text = resume_text

    def get_conversation_history(self):
        return self.memory.buffer

    def generate_question(self):
        conversation_history = self.get_conversation_history()
        question = self.question_agent.generate_question(
            resume_text=self.resume_text,
            conversation_history=conversation_history
        )
        # Update the conversation memory with the question
        self.memory.save_context({"agent": "AI"}, {"message": question})
        return question

    def receive_response(self, user_response):
        # Update the conversation memory with the user's response
        self.memory.save_context({"agent": "User"}, {"message": user_response})

    def start_interview(self):
        if 'current_question' not in st.session_state:
            # Generate the first question
            question = self.generate_question()
            st.session_state['current_question'] = question
        else:
            question = st.session_state['current_question']

        st.write("**Interviewer:**")
        st.write(question)

        candidate_response = st.text_area("Your Response", key='candidate_response')

        if st.button("Submit Response"):
            if candidate_response.strip() == "":
                st.error("Please enter your response before submitting.")
            else:
                # Save the user's response
                self.receive_response(candidate_response)
                # Clear the candidate's response
                st.session_state['candidate_response'] = ""
                # Generate the next question
                next_question = self.generate_question()
                st.session_state['current_question'] = next_question
                # Rerun to display the next question
                st.experimental_rerun()
