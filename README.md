# student-organiser-rag-llm(Flask-Based RAG QA System)

A Flask-based Retrieval-Augmented Generation (RAG) chatbot application that integrates Google's Gemini AI, TF-IDF similarity search, and document retrieval from PDFs and web pages.

💻 Local Setup

Install Python dependencies

pip install -r requirements.txt

Set up the Flask application

Run the Flask app locally:

python app.py

The application will be available at http://127.0.0.1:8080/.

📄 Data Processing

TF-IDF Vectorization: Retrieves the most relevant documents based on cosine similarity.

PDF Extraction: Uses PyPDF2 to extract text from PDF documents.

Web Scraping: Extracts content from web pages using BeautifulSoup.

Keyword Extraction: Implements TF-IDF for key term identification.

🚀 Deployment with Docker

Build and Run the Container

docker build -t flask-rag-app .
docker run -p 8080:8080 flask-rag-app

The app will be accessible at http://localhost:8080/.

🎣 RAG Pipeline Overview

Framework: Flask (Python)

Retrieval: TF-IDF + Cosine Similarity

Vector Database: N/A (TF-IDF-based retrieval)

Language Model: Google Gemini AI

Front-End Chat Interface: Flask + HTML/CSS/JS

📝 Example Queries

"What are the latest advancements in AI?"

"Summarize this PDF document."

"Extract key points from this webpage."

🔬 Performance Evaluation

Query Response Time: ~10-20 seconds

Accuracy: High relevance in retrieval, dependent on Gemini AI’s response generation

Accuracy Evaluation Methodology:

Tested across 10 queries with different complexity levels:

Basic keyword matching

Single-source semantic retrieval

Multi-source semantic retrieval

Scoring: 1 point for correct response & sources, 0.5 for correct sources, 0 for incorrect results.

Achieved Accuracy: 7.5/10

🚀 Future Tasks

Implement ChromaDB for vector-based retrieval.

Cache chat history for a longer context window.

Introduce source prioritization (e.g., FAQ pages).

Deploy on cloud platforms (e.g., AWS, GCP, Nectar).

Scale to larger models for improved accuracy.
