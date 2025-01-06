"""
Backend Logic for Document Q&A Application
- Handles file parsing, retrieval, and AI-powered question answering
"""

import pandas as pd
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load AI models
def load_models():
    """
    Load necessary models:
    - Question-Answering model from Hugging Face
    - Sentence embedding model from Sentence Transformers
    Returns:
        qa_model: Hugging Face pipeline for Q&A
        embedding_model: SentenceTransformer model for embeddings
    """
    qa_model = pipeline("question-answering")
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    return qa_model, embedding_model


# Parse Excel file
def parse_excel(file_path):
    """
    Parse an uploaded Excel file into a list of dictionaries, where each dictionary represents a row.
    Args:
        file_path: Path to the uploaded Excel file
    Returns:
        List of dictionaries representing rows in the Excel file
    """
    try:
        data = pd.read_excel(file_path)
        return data.to_dict(orient="records")
    except Exception as e:
        raise ValueError(f"Error parsing Excel file: {e}")


# Build FAISS retrieval index
def build_index(data, embedding_model):
    """
    Build a FAISS index for retrieving relevant content based on semantic similarity.
    Args:
        data: List of dictionaries representing file content
        embedding_model: SentenceTransformer model for generating embeddings
    Returns:
        index: FAISS index for similarity search
        texts: List of concatenated strings representing each row of data
    """
    try:
        # Combine each row's values into a single string for embedding
        texts = [" ".join(map(str, row.values())) for row in data]
        embeddings = embedding_model.encode(texts, convert_to_tensor=False)

        # Initialize and populate the FAISS index
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(np.array(embeddings))
        return index, texts
    except Exception as e:
        raise ValueError(f"Error building retrieval index: {e}")


# Retrieve relevant content
def retrieve(query, index, texts, embedding_model, top_k=3):
    """
    Retrieve the most relevant content for a given query using semantic similarity.
    Args:
        query: User's question as a string
        index: FAISS index for similarity search
        texts: List of texts corresponding to the document rows
        embedding_model: SentenceTransformer model for query embeddings
        top_k: Number of top matches to return
    Returns:
        List of relevant texts
    """
    try:
        # Generate the query embedding
        query_embedding = embedding_model.encode([query])
        # Search for top_k matches in the FAISS index
        _, indices = index.search(np.array(query_embedding), k=top_k)
        return [texts[i] for i in indices[0]]
    except Exception as e:
        raise ValueError(f"Error retrieving relevant content: {e}")


# Generate answers
def answer_question(query, retrieved_texts, qa_model):
    """
    Generate an answer for a user's query based on retrieved content.
    Args:
        query: User's question as a string
        retrieved_texts: List of relevant texts retrieved from the document
        qa_model: Hugging Face pipeline for Q&A
    Returns:
        String containing the generated answer
    """
    try:
        # Combine retrieved texts into a single context string
        context = " ".join(retrieved_texts)
        # Use the QA model to generate an answer
        result = qa_model(question=query, context=context)
        return result["answer"]
    except Exception as e:
        raise ValueError(f"Error generating answer: {e}")


# Load models globally to avoid reloading
qa_model, embedding_model = load_models()
