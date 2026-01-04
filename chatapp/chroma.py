import chromadb
from django.conf import settings

# Initialize ChromaDB with persistent storage
chroma_client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
collection = chroma_client.get_or_create_collection(name="chatbot_data")
