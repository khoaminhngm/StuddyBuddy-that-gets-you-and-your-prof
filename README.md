# StudyBuddy – AI Tutoring Chatbot

StudyBuddy is your AI-powered learning partner.
It reads your lecture PDFs, understands the content, and answers your questions — in any language, about any topic from your slides.

---

## Project Structure

```plaintext
project-root/
├── client/                 # React frontend
│   ├── src/
│   ├── public/
│   └── package.json
│
├── server/                 # FastAPI backend
│   ├── lecture_pdf/        # Folder for uploaded lecture slides
│   ├── main.py             # FastAPI entrypoint
│   ├── producer.py         # PDF parser and chunk generator
│   ├── consumer.py         # Uploads chunks to vector database
│   ├── llm.py              # Gemini-based LLM handler
│   ├── rag.py              # Retrieval-Augmented Generation logic
│   ├── .env                # API keys (ignored by Git)
│   └── requirements.txt    # Python dependencies
│
└── README.md               # Project guide
```


---

## ⚙️ How to Run

### 1️⃣ Add Lecture Slides

Place your lecture slides into:

/server/lecture_pdf/


### 2️⃣ Install Python Dependencies

Go to the server directory:
```bash
cd server
pip install -r requirements.txt
```

### 3️⃣ Create and Configure .env
Inside /server/, create a file named .env and add your API key (or i sent u my api key privately):
```plaintext
    GOOGLE_API_KEY=your_api_key_here
    PINECONE_API_KEY=your_api_key_here
```
(This file is ignored by Git.)


### 4️⃣ Generate Chunks from PDF
Before running, delete any existing chunks.json in /server. Then run:
```bash
    python producer.py
```
This parses your PDF and saves text chunks for embedding.


### 5️⃣ Upload Chunks to Vector Database
Run:
```bash
    python consumer.py
```
This uploads your generated chunks to the vector store for retrieval.

### 6️⃣ Start the FastAPI Backend
Start the backend server:
```bash
    uvicorn main:app --reload --port 8000

```
Your backend will run on http://localhost:8000

### 7️⃣ Start the React Frontend
Open a new terminal and run:
```bash
cd client
npm install
npm start
```
Your frontend will run on http://localhost:3000


### 8️⃣ Chat with StudyBuddy 🎓
Open your browser at http://localhost:3000,
ask questions about your lecture slides in **any language**,
and StudyBuddy will respond using the content extracted from your PDF.
