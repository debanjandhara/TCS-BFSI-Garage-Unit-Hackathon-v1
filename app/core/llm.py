"""
Language model and embeddings handling for the RAG application
"""

import os
import logging
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from ..utils.config import LLM_MODEL, EMBEDDING_MODEL

def get_embeddings_model():
    """
    Creates an OpenAI embeddings model.
    This is used to convert text into vectors.
    """
    try:
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("Missing OpenAI API Key")
        embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
        logging.info(f"Initialized OpenAI embeddings: {EMBEDDING_MODEL}")
        return embeddings
    except Exception as e:
        logging.error(f"Failed to initialize embeddings model: {e}")
        raise

def get_llm(streaming=False, temperature=0.7):
    """
    Creates an OpenAI language model.
    This is used to generate responses.
    
    Args:
        streaming (bool): Whether to stream responses
        temperature (float): Controls creativity (0.0-1.0)
        
    Returns:
        ChatOpenAI: The configured language model
    """
    try:
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("Missing OpenAI API Key")
        
        llm = ChatOpenAI(
            model_name=LLM_MODEL, 
            temperature=temperature,
            streaming=streaming
        )
        
        logging.info(f"Initialized OpenAI LLM: {LLM_MODEL} (streaming={streaming})")
        return llm
    except Exception as e:
        logging.error(f"Failed to initialize LLM: {e}")
        raise 