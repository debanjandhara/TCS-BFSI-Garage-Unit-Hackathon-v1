"""
Main entry point for the RAG Chatbot application
"""

import streamlit as st
import os
import logging
import sys

# Add parent directory to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import our application components
from app.utils.config import ensure_directories
from app.utils.logging_utils import setup_logging
from app.utils.session import initialize_session_state
from app.core.llm import get_embeddings_model, get_llm
from app.core.vector_store import load_vector_store
from app.ui.sidebar import render_sidebar
from app.ui.chat import render_chat_ui

# Configure the Streamlit page
st.set_page_config(page_title="RAG Chatbot", layout="wide")

def initialize_app():
    """
    Initialize the application:
    1. Set up logging
    2. Ensure necessary directories exist
    3. Initialize session state
    4. Load models and vector store if API key is provided
    """
    # Set up logging
    setup_logging()
    
    # Ensure necessary directories exist
    ensure_directories()
    
    # Initialize session state
    initialize_session_state()
    
    # If we have an API key, load models and vector store
    if st.session_state.openai_api_key_provided:
        try:
            # Load embeddings model if not already loaded
            if st.session_state.embeddings_model is None:
                st.session_state.embeddings_model = get_embeddings_model()
                
            # Load LLM if not already loaded
            if st.session_state.llm is None:
                # Load a streaming LLM for the chat interface
                st.session_state.llm = get_llm(streaming=True)
                
            # Mark models as loaded
            st.session_state.models_loaded = True
            
            # Try to load vector store if models are loaded
            if st.session_state.models_loaded and st.session_state.vector_store is None:
                st.session_state.vector_store = load_vector_store(st.session_state.embeddings_model)
                if st.session_state.vector_store:
                    st.session_state.vector_store_loaded = True
                    logging.info("Vector store loaded successfully.")
                else:
                    st.session_state.vector_store_loaded = False
                    logging.warning("Vector store not found or failed to load.")
                    
        except Exception as e:
            st.sidebar.error(f"Failed to initialize OpenAI models: {e}")
            st.session_state.models_loaded = False
            logging.error(f"Failed to initialize models: {e}", exc_info=True)

def main():
    """Main application function"""
    # Initialize the app
    initialize_app()
    
    # Render the sidebar
    mode_text = render_sidebar()
    
    # Render the chat UI
    render_chat_ui(mode_text)

if __name__ == "__main__":
    main() 