"""
Vector store handling for the RAG application
"""

import os
import logging
from langchain_community.vectorstores import FAISS
from ..utils.config import VECTORSTORE_PATH
from .document_store import split_documents

def create_vector_store(docs, embeddings_model):
    """
    Creates a FAISS vector store from documents.
    This is where we convert text into searchable vectors.
    
    Args:
        docs (list): List of documents to index
        embeddings_model: The embeddings model to use
        
    Returns:
        FAISS: The vector store or None if fails
    """
    if not docs:
        logging.warning("No documents provided for vector store creation.")
        return None
        
    try:
        # Split documents into smaller chunks for better retrieval
        splits = split_documents(docs)
        
        if not splits:
            logging.warning("Document splitting resulted in zero chunks.")
            return None
        
        # Create and save the vector store
        vs_dir = os.path.dirname(VECTORSTORE_PATH)
        os.makedirs(vs_dir, exist_ok=True)
        
        vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings_model)
        vectorstore.save_local(VECTORSTORE_PATH)
        
        logging.info(f"FAISS index created with {len(splits)} chunks, saved to {VECTORSTORE_PATH}")
        return vectorstore
        
    except Exception as e:
        logging.error(f"Failed to create vector store: {e}", exc_info=True)
        return None

def load_vector_store(embeddings_model):
    """
    Loads an existing FAISS vector store from disk.
    This is faster than recreating it from documents.
    
    Args:
        embeddings_model: The embeddings model to use
        
    Returns:
        FAISS: The vector store or None if fails
    """
    if os.path.exists(VECTORSTORE_PATH) and os.path.isdir(VECTORSTORE_PATH):
        faiss_file = os.path.join(VECTORSTORE_PATH, "index.faiss")
        pkl_file = os.path.join(VECTORSTORE_PATH, "index.pkl")
        
        if os.path.isfile(faiss_file) and os.path.isfile(pkl_file):
            try:
                vectorstore = FAISS.load_local(
                    VECTORSTORE_PATH, 
                    embeddings_model, 
                    allow_dangerous_deserialization=True
                )
                logging.info(f"Loaded FAISS index from {VECTORSTORE_PATH}")
                return vectorstore
                
            except Exception as e:
                logging.error(f"Failed to load FAISS index: {e}", exc_info=True)
                return None
        else:
            logging.warning(f"FAISS index files not found in {VECTORSTORE_PATH}.")
            return None
    else:
        logging.warning(f"FAISS index directory not found at {VECTORSTORE_PATH}.")
        return None 