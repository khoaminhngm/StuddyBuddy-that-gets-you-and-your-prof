from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from dotenv import load_dotenv

from consumer import StudyBuddyIndexer
from rag import RAGSystem
from llm import LLM_Tutor
from producer import PDFChunker

app = FastAPI(title="StudyBuddy API", version="1.0")
rag = RAGSystem(indexer=StudyBuddyIndexer())
load_dotenv()

# --- CORS middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Define request / response models ---
class StudyBuddyRequest(BaseModel):
    prompt: str  


class StudyBuddyResponse(BaseModel):
    response: str
    total_chunks: int
    sample_chunks: str  


# --- POST endpoint ---
@app.post("/", response_model=StudyBuddyResponse)
async def study_buddy(payload: StudyBuddyRequest):
    """
    Input:  user prompt (string)
    Output: confirmation with total chunks and preview
    """

    chunks, length = rag.retrieve_relevant_chunks(query=payload.prompt, top_k=4)

    llm = LLM_Tutor(rag_system=rag)
    answer = llm.answer_question(student_question=payload.prompt)
    res = llm.translate_response(response=answer, target_language="Chinese")

    return StudyBuddyResponse(
        response=res,
        total_chunks=length,
        sample_chunks=chunks  # only show first few for clarity
    )


@app.get("/")
def root():
    return {"message": "Hello StudyBuddy!"}