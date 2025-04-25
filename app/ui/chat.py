"""
Chat UI components for the Streamlit application
"""

import streamlit as st
import time
import logging
from ..core.rag_engine import get_streaming_answer

def render_chat_header(session_name, mode_text):
    """Render the chat header with session name and mode"""
    st.title(f"💬 Chat: {session_name}")
    st.caption(f"Mode: {mode_text}")

def render_chat_history(current_session):
    """Render the chat history with messages"""
    # Display all messages in the history
    for i, (human_msg, ai_msg) in enumerate(current_session["history"]):
        with st.chat_message("user"):
            st.write(human_msg)
            
        with st.chat_message("assistant"):
            st.write(ai_msg)

def render_chat_input(current_sid):
    """Render the chat input area"""
    # Simple chat input box
    user_query = st.chat_input("Ask a question about your documents:", key=f"chat_input_{current_sid}")
    return user_query

def handle_user_input(user_query, current_sid):
    """Process user input and generate AI response"""
    if not user_query:
        return

    current_session = st.session_state.chat_sessions[current_sid]

    # Check if we can process the query
    if not st.session_state.get("vector_store_loaded", False):
        st.warning("Please index your documents before asking questions.")
        return
    elif not st.session_state.get("models_loaded", False):
        st.error("Cannot process query: OpenAI models not loaded (check API key).")
        return

    # Add the user's message to history right away (with empty AI response)
    st.session_state.chat_sessions[current_sid]["history"].append((user_query, ""))

    # Show the user's message
    with st.chat_message("user"):
        st.write(user_query)

    # Show AI thinking...
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        try:
            # Get previous messages for context (excluding the current one)
            raw_history_tuples = current_session["history"][:-1]

            # Time the response for monitoring
            start_time = time.time()
            
            # Use streaming answer
            answer_text = ""
            
            # Stream the response
            for chunk in get_streaming_answer(
                query=user_query,
                chat_history=raw_history_tuples,
                vectorstore=st.session_state.vector_store,
                llm=st.session_state.llm,
                chatgpt_enabled=st.session_state.chatgpt_enabled
            ):
                answer_text += chunk
                message_placeholder.markdown(answer_text + "▌")
                time.sleep(0.01)  # Small delay for smoother streaming
            
            # Update with final text (remove the cursor)
            message_placeholder.markdown(answer_text)
            
            # Update history with the AI's response
            st.session_state.chat_sessions[current_sid]["history"][-1] = (user_query, answer_text)
            
            end_time = time.time()
            logging.info(f"Query processed in {end_time - start_time:.2f} seconds.")
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
            logging.error(f"Error processing query: {e}", exc_info=True)
            # Remove the placeholder history entry if an error occurs
            st.session_state.chat_sessions[current_sid]["history"].pop()

def render_chat_ui(mode_text):
    """Render the entire chat UI"""
    current_sid = st.session_state.current_session_id
    current_session = st.session_state.chat_sessions[current_sid]
    
    # Show current chat name and mode
    render_chat_header(current_session["name"], mode_text)
    
    # Display the chat history
    render_chat_history(current_session)
    
    # Chat input
    user_query = render_chat_input(current_sid)
    
    # Process user input
    handle_user_input(user_query, current_sid) 