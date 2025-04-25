"""
Session state management for the Streamlit application
"""

import streamlit as st
import uuid
import logging

def initialize_session_state():
    """
    Initialize or update session state variables for the application
    """
    # Check if the session has been initialized
    if "initialized" not in st.session_state:
        st.session_state.initialized = False

    # Initialize OpenAI API key tracking
    if "openai_api_key_provided" not in st.session_state:
        st.session_state.openai_api_key_provided = False
    
    # Initialize model tracking
    if "models_loaded" not in st.session_state:
        st.session_state.models_loaded = False
    
    # Initialize embeddings model
    if "embeddings_model" not in st.session_state:
        st.session_state.embeddings_model = None
    
    # Initialize LLM
    if "llm" not in st.session_state:
        st.session_state.llm = None
    
    # Initialize vector store
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
        st.session_state.vector_store_loaded = False
    
    # Initialize chat sessions
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = {}  # Format: {session_id: {"name": str, "history": List[Tuple(str,str)]}}
    
    # Initialize current session ID
    if "current_session_id" not in st.session_state:
        # Create first chat session
        first_session_id = str(uuid.uuid4())
        st.session_state.chat_sessions[first_session_id] = {"name": "Chat 1", "history": []}
        st.session_state.current_session_id = first_session_id
    
    # Initialize ChatGPT mode toggle
    if "chatgpt_enabled" not in st.session_state:
        st.session_state.chatgpt_enabled = True  # Default to using both RAG and ChatGPT
    
    # Initialize streaming state
    if "generate_active" not in st.session_state:
        st.session_state.generate_active = False
    
    # Set the initialization flag
    if not st.session_state.initialized:
        st.session_state.initialized = True
        logging.info("Session state initialized") 