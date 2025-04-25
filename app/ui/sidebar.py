"""
Sidebar UI components for the Streamlit application
"""

import os
import streamlit as st
import logging
import uuid
from .document_management import render_document_management

def render_api_key_input():
    """Render the API key input section in the sidebar"""
    st.sidebar.title("Configuration")
    
    # Check if API key is already in environment (loaded from .env)
    if os.environ.get("OPENAI_API_KEY") and not st.session_state.get("openai_api_key_provided", False):
        st.session_state.openai_api_key_provided = True
        
    # Show API key status
    if st.session_state.get("openai_api_key_provided", False):
        st.sidebar.success("OpenAI API Key Loaded.")
    else:
        api_key = st.sidebar.text_input("Enter OpenAI API Key:", type="password", key="api_key_input")
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            st.session_state.openai_api_key_provided = True
            st.sidebar.success("OpenAI API Key Loaded.")
            st.rerun()
        else:
            st.sidebar.warning("OpenAI API Key needed.")

def render_mode_toggle():
    """Render the ChatGPT mode toggle in the sidebar"""
    st.session_state.chatgpt_enabled = st.sidebar.toggle(
        "Enable ChatGPT Knowledge",
        value=st.session_state.get("chatgpt_enabled", True),
        key="chatgpt_mode_toggle",
        help="ON: Use Vector DB + ChatGPT knowledge. OFF: Use Vector DB knowledge ONLY."
    )
    
    mode_text = "RAG + LLM" if st.session_state.chatgpt_enabled else "RAG Only (Strict)"
    st.sidebar.caption(f"Current Mode: {mode_text}")
    
    return mode_text

def render_chat_session_management():
    """Render the chat session management section in the sidebar"""
    st.sidebar.subheader("Chat Sessions")
    
    # Button to create a new chat session
    if st.sidebar.button("➕ New Chat", key="new_chat_button"):
        new_session_id = str(uuid.uuid4())
        session_count = len(st.session_state.chat_sessions) + 1
        st.session_state.chat_sessions[new_session_id] = {"name": f"Chat {session_count}", "history": []}
        st.session_state.current_session_id = new_session_id
        st.rerun()  # Refresh to show new chat
    
    # Show all chat sessions with rename/delete options
    sorted_session_ids = sorted(st.session_state.chat_sessions.keys())  # Keep order consistent
    for session_id in sorted_session_ids:
        session_name = st.session_state.chat_sessions[session_id]["name"]
        
        # Create a row for each chat with buttons
        col1, col2, col3 = st.sidebar.columns([3, 1, 1])
        
        # Highlight the current session with the chat name button
        button_type = "primary" if session_id == st.session_state.current_session_id else "secondary"
        if col1.button(session_name, key=f"session_btn_{session_id}", use_container_width=True, type=button_type):
            st.session_state.current_session_id = session_id
            st.rerun()
        
        # Rename button (shows a modal dialog)
        if col2.button("✏️", key=f"rename_btn_{session_id}", help="Rename chat"):
            st.session_state.renaming_session_id = session_id
            st.session_state.show_rename_modal = True
        
        # Delete button (with confirmation)
        if col3.button("🗑️", key=f"delete_btn_{session_id}", help="Delete chat"):
            st.session_state.deleting_session_id = session_id
            st.session_state.show_delete_modal = True
    
    # Rename modal dialog
    if st.session_state.get("show_rename_modal", False):
        with st.sidebar.popover("Rename Chat", use_container_width=True):
            session_id = st.session_state.renaming_session_id
            current_name = st.session_state.chat_sessions[session_id]["name"]
            new_name = st.text_input("New name:", value=current_name, key="new_chat_name")
            col1, col2 = st.columns(2)
            if col1.button("Cancel", key="cancel_rename"):
                st.session_state.show_rename_modal = False
                st.rerun()
            if col2.button("Save", key="save_rename", type="primary"):
                st.session_state.chat_sessions[session_id]["name"] = new_name
                st.session_state.show_rename_modal = False
                st.rerun()
    
    # Delete confirmation modal
    if st.session_state.get("show_delete_modal", False):
        with st.sidebar.popover("Delete Chat?", use_container_width=True):
            st.write("Are you sure you want to delete this chat?")
            col1, col2 = st.columns(2)
            if col1.button("Cancel", key="cancel_delete"):
                st.session_state.show_delete_modal = False
                st.rerun()
            if col2.button("Delete", key="confirm_delete", type="primary"):
                delete_session(st.session_state.deleting_session_id)
                st.session_state.show_delete_modal = False
                st.rerun()

def delete_session(session_id):
    """Delete a chat session and switch to another session"""
    if session_id in st.session_state.chat_sessions:
        del st.session_state.chat_sessions[session_id]
        # Select another session if available, otherwise create a new one
        if st.session_state.chat_sessions:
            st.session_state.current_session_id = next(iter(st.session_state.chat_sessions))
        else:
            # Create a new chat if no others exist
            new_session_id = str(uuid.uuid4())
            st.session_state.chat_sessions[new_session_id] = {"name": "Chat 1", "history": []}
            st.session_state.current_session_id = new_session_id

def render_sidebar():
    """Render the entire sidebar UI"""
    render_api_key_input()
    mode_text = render_mode_toggle()
    render_chat_session_management()
    render_document_management()
    
    return mode_text 