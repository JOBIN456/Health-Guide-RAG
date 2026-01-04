HealthGuide RAG is an AI-powered healthcare assistant that provides accurate, context-aware responses to health-related questions using Retrieval-Augmented Generation (RAG) and the Ollama LLM. The system retrieves relevant medical information and generates intelligent answers for users in real time.

Features

AI-Powered Q&A: Provides answers to health queries using RAG and Ollama LLM.

Context-Aware Responses: Retrieves relevant data to deliver accurate, reliable information.

Secure: Sensitive credentials are managed through .env files.

Extensible: Easy to integrate new datasets or extend LLM capabilities.

Tech Stack

Backend: Python, Django

AI/LLM: Ollama, LangChain, RAG

Database: ChromaDB (vector database for retrieval)

Frontend: HTML, CSS, JavaScript


Installation & Setup

Clone the repository:

git clone https://github.com/JOBIN456/Health-Guide-RAG.git


Navigate to the project folder:

cd Health-Guide-RAG


Create a .env file in the project root (use .env.example as a template):

OLLAMA_KEY=your_ollama_key_here


Install dependencies:

pip install -r requirements.txt


Run migrations:

python manage.py migrate


Start the server:

python manage.py runserver
