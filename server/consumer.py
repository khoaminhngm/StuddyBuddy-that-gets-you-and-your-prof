import json
import getpass
import os
from uuid import uuid4
from pinecone import Pinecone
from langchain_pinecone import PineconeEmbeddings, PineconeVectorStore
from langchain_core.documents import Document
from dotenv import load_dotenv


class StudyBuddyIndexer:
    def __init__(self, json_path="chunks.json", index_name="llama-text-embed-v2"):
        """Initialize the StudyBuddyIndexer."""
        load_dotenv()
        # Load Pinecone API key
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        os.environ["PINECONE_API_KEY"] = self.pinecone_api_key

        # Connect to Pinecone
        self.pc = Pinecone(api_key=self.pinecone_api_key)
        self.index_name = index_name
        self.json_path = json_path

        # Load JSON chunks
        with open(self.json_path, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)
        print(f"✅ Loaded {len(self.chunks)} chunks from {self.json_path}")

        # Initialize Pinecone index
        if not self.pc.has_index(self.index_name):
            self.pc.create_index_for_model(
                name=self.index_name,
                cloud="aws",
                region="us-east-1",
                embed={"model": "llama-text-embed-v2", "field_map": {"text": "text"}},
            )
            print(f"🆕 Created Pinecone index '{self.index_name}'")

        self.index = self.pc.Index(self.index_name)

        # Initialize embeddings & vector store
        self.embeddings = PineconeEmbeddings(model="llama-text-embed-v2")
        self.vector_store = PineconeVectorStore(index=self.index, embedding=self.embeddings)

    def prepare_documents(self):
        """Convert JSON chunks into LangChain Document objects."""
        documents = []
        for i, text in enumerate(self.chunks):
            doc = Document(
                page_content=text,
                metadata={"source": "lecture_slide", "chunk_id": i},
            )
            documents.append(doc)
        print(f"📝 Prepared {len(documents)} Document objects.")
        return documents
    
    def clear_index(self):
        self.vector_store.delete(delete_all=True)

    def upload_documents(self):
        """Upload parsed documents to Pinecone."""
        self.clear_index()
        documents = self.prepare_documents()
        uuids = [str(uuid4()) for _ in range(len(documents))]
        self.vector_store.add_documents(documents=documents, ids=uuids)
        print(f"✅ Uploaded {len(documents)} documents to Pinecone index '{self.index_name}'.")

    def clear_index(self):
        """Optional: Delete and recreate the index (use carefully)."""
        if self.pc.has_index(self.index_name):
            self.pc.delete_index(self.index_name)
            print(f"🗑️ Deleted old index '{self.index_name}'")
        self.pc.create_index_for_model(
            name=self.index_name,
            cloud="aws",
            region="us-east-1",
            embed={"model": "llama-text-embed-v2", "field_map": {"text": "text"}},
        )
        print(f"🔁 Recreated index '{self.index_name}'")


if __name__ == "__main__":
    indexer = StudyBuddyIndexer(json_path="chunks.json", index_name="llama-text-embed-v2")
    indexer.upload_documents()