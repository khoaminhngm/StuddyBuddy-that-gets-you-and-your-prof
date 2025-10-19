import consumer
from llm import LLM_Tutor
from dotenv import load_dotenv


class RAGSystem:
    def __init__(self, indexer: consumer.StudyBuddyIndexer):
        self.indexer = indexer
        self.vector_store = indexer.vector_store
        # Initialize a tutor with this RAG system (so it can access the same context if needed)
        self.llm_tutor = LLM_Tutor(self)
        load_dotenv()

    def translate_query(self, query: str, target_language: str = "German") -> str:
        """
        Translate the input query to the target language using Gemini via LLM_Tutor.
        Default target language: German.
        """
        print(f"🌍 Translating query to {target_language}...")
        try:
            translated = self.llm_tutor.translate_response(query, target_language)
            return translated
        except Exception as e:
            print(f"⚠️ Translation failed: {e}")
            return query 

    def retrieve_relevant_chunks(self, query: str, top_k: int = 5):
        """
        Retrieve the most relevant chunks for a given query.
        """
        translated = self.translate_query(query, target_language="German")
        retrieved = self.vector_store.similarity_search_with_relevance_scores(query=translated, k=top_k)
        relevant_string = "\n\n".join([f"- {doc.page_content}\n Score: {score}" for doc, score in retrieved])
        return relevant_string, len(retrieved)
