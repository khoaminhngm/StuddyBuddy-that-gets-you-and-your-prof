# Not implemented in API yet.. just run it manually first haha

from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
import os


class PDFChunker:
    """Class to parse a PDF file, split it into text chunks, and save as JSON."""

    def __init__(self, pdf_path, chunk_size=1000, overlap=100, output_path="chunks.json"):
        self.pdf_path = pdf_path
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.output_path = output_path

    def extract_text(self):
        """Extracts text from the PDF."""
        if not os.path.exists(self.pdf_path):
            raise FileNotFoundError(f"PDF file not found: {self.pdf_path}")

        reader = PdfReader(self.pdf_path)
        text = "\n".join([page.extract_text() or "" for page in reader.pages])
        return text

    def chunk_text(self, text):
        """Splits the text into overlapping chunks."""
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.overlap
        )
        chunks = splitter.split_text(text)
        return chunks

    def save_chunks(self, chunks):
        """Saves the chunks into a JSON file."""
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)

    def run(self):
        """Main pipeline: extract, chunk, save."""
        print(f"📄 Parsing PDF: {self.pdf_path}")
        text = self.extract_text()
        print(f"✅ Extracted {len(text)} characters.")

        chunks = self.chunk_text(text)
        print(f"🔹 Created {len(chunks)} chunks (size={self.chunk_size}, overlap={self.overlap}).")

        self.save_chunks(chunks)
        print(f"💾 Saved to {self.output_path}")

        return chunks


if __name__ == "__main__":
    pdf_path = "lecture_pdf/lecture_slides.pdf"
    chunker = PDFChunker(pdf_path, chunk_size=1000, overlap=100)
    chunker.run()
