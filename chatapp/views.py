from django.shortcuts import render,redirect
from .models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET,require_POST
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
import json
from django.http import JsonResponse
from langchain.embeddings import OllamaEmbeddings
from .chroma import collection  # Import ChromaDB collection
import os
from django.conf import settings
# Create your views here.
import groq
import numpy as np



def login_view(request):
    return render(request,'login.html')

def register(request):
    return render(request,'register.html')


@require_POST
def loginsubmit(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"status": 200, "message": "Login successful" ,"redirect":"/home/"})
    else:
        return JsonResponse({"status": 401, "message": "Invalid credentials"}, status=401)

@require_POST
def registersubmit(request):
    username = request.POST.get("username")
    password1 = request.POST.get("password1")
    password2 = request.POST.get("password2")

    # Basic validation
    if not username or not password1 or not password2:
        return JsonResponse({"status": 400, "message": "All fields are required"}, status=400)

    if password1 != password2:
        return JsonResponse({"status": 400, "message": "Passwords do not match"}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({"status": 409, "message": "Username already exists"}, status=409)

    User.objects.create_user(username=username, password=password1)

    return JsonResponse({"status": 200, "message": "Registration successful", "redirect": "/"})
@require_POST
def logout_view(request):
    logout(request)
    return redirect("login_view")  

    
@login_required
def home(request):
    return render(request,'chat.html')






















embedding_model = OllamaEmbeddings(model="nomic-embed-text")
# THE VECTOR TRANSFORMATION OF TEXT


def store_json_data(request):
    """
    Reads JSON files from the project's dataset folder and stores them in ChromaDB.
    Uses LangChain's OllamaEmbeddings for embedding generation.
    """
    folder_path = os.path.join(settings.BASE_DIR, "dataset")  # Adjust this path
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                    text = json.dumps(data)  # Convert JSON to string
                    
                    # ✅ Use LangChain's OllamaEmbeddings
                    embedding = embedding_model.embed_documents([text])[0]  # Extract embedding vector
                    
                    # Store in ChromaDB
                    collection.add(
                        ids=[filename], 
                        embeddings=[embedding],
                        metadatas=[{"filename": filename, "content": text}]
                    )
                    
                except Exception as e:
                    return JsonResponse({"status": "error", "message": str(e)})
    
    return JsonResponse({"status": "success", "message": "Data stored in ChromaDB"})

# def store_json_data(request):
#     """
#     Reads JSON files from the project's dataset folder and stores them in ChromaDB.
#     Uses Ollama's 'nomic-embed-text' model for embeddings.
#     """
#     folder_path = os.path.join(settings.BASE_DIR, "dataset")  # Adjust this path
    
#     for filename in os.listdir(folder_path):
#         if filename.endswith(".json"):
#             file_path = os.path.join(folder_path, filename)
            
#             with open(file_path, "r", encoding="utf-8") as file:
#                 try:
#                     data = json.load(file)
#                     text = json.dumps(data)  # Convert JSON to string
                    
#                     # ✅ Use Ollama's local embedding model
#                     response = ollama.embeddings(model="nomic-embed-text", prompt=text)
#                     embedding = response["embedding"]  # Extract embedding vector
                    
#                     # Store in ChromaDB
#                     collection.add(
#                         ids=[filename], 
#                         embeddings=[embedding],
#                         metadatas=[{"filename": filename, "content": text}]
#                     )
                    
#                 except Exception as e:
#                     return JsonResponse({"status": "error", "message": str(e)})
    
#     return JsonResponse({"status": "success", "message": "Data stored in ChromaDB"})




















client = groq.Client(api_key=settings.GROQ_API_KEY)  # Initialize Groq Client

@require_POST
def message(request):
    user_message = request.POST.get("message", "").strip()
    
    if not user_message:
        return JsonResponse({"error": "Message cannot be empty"}, status=400)

    try:
        # Step 1: Convert user message into an embedding
        query_embedding = embedding_model.embed_documents([user_message])[0]
        
        # Step 2: Retrieve relevant documents from ChromaDB
        results = collection.query(
            query_embeddings=[query_embedding], 
            n_results=3  # Retrieve top 3 matches
        )
        
        # ✅ Fix: Ensure retrieved documents are valid strings
        retrieved_docs = results.get("documents", [[]])[0]  # Get first set of documents
        retrieved_context = "\n".join([doc for doc in retrieved_docs if isinstance(doc, str)])  # Filter out None values

        if not retrieved_context:
            retrieved_context = "No relevant context found."

        # Step 3: Generate response using Groq API with retrieved context
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": f"You are an intelligent chatbot. Use the following information if relevant: {retrieved_context}"},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=700  
        )

        bot_reply = response.choices[0].message.content.strip() if response.choices else "I'm not sure."
        
        return JsonResponse({"success": True, "message": bot_reply})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)





# for testing


def get_full_chroma_collection(request):
    """
    Retrieves and prints all stored data in ChromaDB collection.
    Converts NumPy arrays to lists for JSON serialization.
    """
    try:
        # Initialize ChromaDB client
       

        # Retrieve all stored documents
        all_docs = collection.peek(100)  # Fetch up to 100 records

        # Convert NumPy arrays (ndarray) to lists
        all_docs["embeddings"] = [embedding.tolist() if isinstance(embedding, np.ndarray) else embedding for embedding in all_docs.get("embeddings", [])]

        return JsonResponse({"success": True, "data": all_docs})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)