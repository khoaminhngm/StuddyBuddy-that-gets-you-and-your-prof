import os
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

class LLM_Tutor:
    def __init__(self, rag_system: "RAGSystem"):  # <- use string type hint
        self.rag_system = rag_system
        load_dotenv()

    def answer_question(self, student_question: str) -> str:
        relevant_chunks_str, _ = self.rag_system.retrieve_relevant_chunks(query=student_question, top_k=4)

        prompt_template = PromptTemplate.from_template(
            """You are an expert in computer science and currently tutoring a university student.

            Based only on the following relevant chunks of information:
            {relevant_chunks}

            answer the student's question clearly, step-by-step, and with intuitive explanations:
            {student_question}
            """
        )

        message = prompt_template.invoke({
            "relevant_chunks": relevant_chunks_str,
            "student_question": student_question
        })

        llm = GoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

        response = llm.invoke(message)
        return response

    def translate_response(self, response: str, target_language: str) -> str:
        prompt_template = PromptTemplate.from_template(
            """Translate the following text into {target_language} while maintaining its original meaning and context:
            {response}
            """
        )

        message = prompt_template.invoke({
            "target_language": target_language,
            "response": response
        })

        llm = GoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

        translated_response = llm.invoke(message)
        return translated_response
