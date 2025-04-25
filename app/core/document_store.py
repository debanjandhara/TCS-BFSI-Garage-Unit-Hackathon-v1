"""
Document loading and processing for the RAG application
"""

import os
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
    UnstructuredFileLoader
)
from ..utils.config import DATA_PATH

def load_documents(directory_path=DATA_PATH):
    """
    Loads all documents from a directory.
    Supports various file types (PDF, TXT, MD, etc.) using different loaders.
    
    Args:
        directory_path (str): Path to directory containing documents
        
    Returns:
        list: List of loaded documents
    """
    docs = []
    if not os.path.exists(directory_path):
        logging.warning(f"Data directory '{directory_path}' not found.")
        return docs
        
    if not os.listdir(directory_path):
        logging.warning(f"Data directory '{directory_path}' is empty.")
        return docs
        
    logging.info(f"Attempting to load documents from: {directory_path}")
    
    try:
        # Use DirectoryLoader to automatically detect and load different file types
        loader = DirectoryLoader(
            directory_path, 
            glob="**/*.*", 
            use_multithreading=True,
            show_progress=True, 
            silent_errors=True, 
            recursive=True
        )
        
        loaded_docs = loader.load()
        
        if not loaded_docs:
             logging.warning(f"No documents successfully loaded from {directory_path}. Check files and dependencies ('unstructured', etc.).")
        else:
            # Clean up any invalid documents
            loaded_docs = [doc for doc in loaded_docs if doc is not None and hasattr(doc, 'page_content') and doc.page_content.strip()]
            docs.extend(loaded_docs)
            logging.info(f"Loaded {len(docs)} document objects from {directory_path}.")
    except ImportError as ie:
         logging.error(f"ImportError during loading: {ie}. Ensure 'unstructured' and parsers are installed.", exc_info=True)
    except Exception as e:
        logging.error(f"Error using DirectoryLoader for {directory_path}: {e}", exc_info=True)
        
    if not docs:
        logging.warning(f"Finished loading. Zero valid documents loaded from '{directory_path}'.")
        
    return docs

def split_documents(docs, chunk_size=1000, chunk_overlap=200):
    """
    Split documents into smaller chunks for better retrieval.
    
    Args:
        docs (list): List of documents to split
        chunk_size (int): Maximum size of each chunk
        chunk_overlap (int): Overlap between chunks
        
    Returns:
        list: List of document chunks
    """
    if not docs:
        logging.warning("No documents provided for splitting.")
        return []
        
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap, 
            length_function=len
        )
        
        splits = text_splitter.split_documents(docs)
        
        if not splits:
            logging.warning("Document splitting resulted in zero chunks.")
            return []
            
        logging.info(f"Split {len(docs)} documents into {len(splits)} text chunks.")
        return splits
        
    except Exception as e:
        logging.error(f"Error splitting documents: {e}", exc_info=True)
        return [] 