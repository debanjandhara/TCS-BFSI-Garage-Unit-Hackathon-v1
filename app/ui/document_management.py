"""
Document management UI components for the Streamlit application
"""

import os
import streamlit as st
import logging
from ..utils.config import DATA_PATH
from ..core.document_store import load_documents
from ..core.vector_store import create_vector_store

def get_file_icon(filename):
    """
    Get the appropriate icon for a file based on its extension
    
    Args:
        filename (str): Name of the file
        
    Returns:
        str: Unicode icon representing the file type
    """
    extension = filename.split('.')[-1].lower()
    if extension in ['csv', 'xls', 'xlsx']:
        return "📊"  # Excel/CSV icon
    elif extension == 'txt':
        return "📄"  # Text file icon
    elif extension == 'json':
        return "📋"  # JSON icon
    elif extension in ['doc', 'docx']:
        return "📝"  # Word document icon
    elif extension == 'pdf':
        return "📑"  # PDF icon
    elif extension == 'md':
        return "📑"  # Markdown icon
    else:
        return "📁"  # Default file icon

def render_document_list():
    """
    Render the list of already indexed documents
    """
    st.sidebar.subheader("Already Indexed Documents")
    
    # Check if vector store exists and load document list
    if st.session_state.get("vector_store_loaded", False):
        # List files in the data directory
        if os.path.exists(DATA_PATH):
            files = [f for f in os.listdir(DATA_PATH) if os.path.isfile(os.path.join(DATA_PATH, f))]
            
            if files:
                for file in files:
                    col1, col2, col3 = st.sidebar.columns([1, 5, 1])
                    file_icon = get_file_icon(file)
                    col1.text(f"{file_icon}")
                    col2.text(f"{file}")
                    if col3.button("🗑️", key=f"delete_{file}", help=f"Delete {file}"):
                        try:
                            os.remove(os.path.join(DATA_PATH, file))
                            st.sidebar.success(f"Deleted: {file}")
                            st.rerun()
                        except Exception as e:
                            st.sidebar.error(f"Error deleting file: {e}")
            else:
                st.sidebar.info("No documents indexed yet.")
        else:
            st.sidebar.info("No documents indexed yet.")
    else:
        st.sidebar.info("Vector store not loaded. Upload and index documents to get started.")

def render_document_upload():
    """
    Render the document upload UI
    """
    st.sidebar.subheader("Upload Documents")
    
    # File uploader with supported file types
    uploaded_files = st.sidebar.file_uploader(
        "Upload documents to index", 
        accept_multiple_files=True, 
        type=["pdf", "txt", "csv", "xlsx", "docx", "json", "md"]
    )
    
    if uploaded_files:
        # Prepare data directory
        os.makedirs(DATA_PATH, exist_ok=True)
        
        # Save uploaded files
        for uploaded_file in uploaded_files:
            # Create a safe filename
            file_path = os.path.join(DATA_PATH, uploaded_file.name)
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.sidebar.success(f"Saved: {uploaded_file.name}")
        
        # Index after upload
        if st.sidebar.button("Index Uploaded Documents", key="index_uploaded"):
            with st.spinner("Indexing uploaded documents..."):
                try:
                    # Load and process documents
                    docs = load_documents(DATA_PATH)
                    if docs:
                        # Create the vector store
                        vs = create_vector_store(docs, st.session_state.embeddings_model)
                        if vs:
                            st.session_state.vector_store = vs
                            st.session_state.vector_store_loaded = True
                            st.sidebar.success("Indexing complete!")
                            st.rerun()
                        else:
                            st.sidebar.error("Indexing failed. Check logs.")
                    else:
                        st.sidebar.warning("No documents found or loaded for indexing.")
                except Exception as e:
                    st.sidebar.error(f"Indexing error: {e}")
                    logging.error(f"Indexing error: {e}", exc_info=True)

def render_document_management():
    """
    Render the document management UI components
    """
    st.sidebar.markdown("---")
    st.sidebar.subheader("Document Management")
    
    render_document_list()
    render_document_upload() 