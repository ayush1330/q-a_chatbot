# agents/question_generation_agent.py

from langchain import OpenAI, LLMChain, PromptTemplate


class QuestionGenerationAgent:
    def __init__(self, api_key):
        # Initialize the OpenAI LLM with your API key
        self.llm = OpenAI(openai_api_key=api_key)

        # Define the prompt template for generating questions
        self.prompt = PromptTemplate(
            input_variables=["resume", "history"],
            template="""
                You are an AI interviewer. Based on the candidate's resume and the conversation history, generate one thoughtful and unique interview question that explores the candidate's experience in more depth.

                Resume:
                {resume}

                Conversation History:
                {history}

                Interview Question:
            """,
        )

        # Create an LLMChain with the prompt template
        self.question_chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def generate_question(self, resume_text, conversation_history):
        # Use the chain to generate a question
        question = self.question_chain.run(
            resume=resume_text, history=conversation_history
        )
        return question.strip()
