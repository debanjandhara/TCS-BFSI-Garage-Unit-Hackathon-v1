"""
Core RAG (Retrieval Augmented Generation) implementation
"""

import logging
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import get_buffer_string
from ..config.prompts import (
    CONDENSE_QUESTION_PROMPT,
    ANSWER_PROMPT,
    RAG_ONLY_ANSWER_PROMPT
)

def create_rag_only_chain(vectorstore, llm):
    """
    Creates a chain that only uses document knowledge (no ChatGPT).
    This is for when users want strict, document-only responses.
    
    Args:
        vectorstore: The vector store for document retrieval
        llm: The language model to use
        
    Returns:
        chain: The RAG-only chain
    """
    if vectorstore is None:
        logging.error("Vector store is None for RAG-only chain.")
        return None
        
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    
    def format_docs(docs): 
        return "\n\n".join(doc.page_content for doc in docs)
        
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | RAG_ONLY_ANSWER_PROMPT
        | llm
        | StrOutputParser()
    )
    
    logging.info("Created RAG-only LCEL chain with RAG-only prompt.")
    return rag_chain

def get_answer(query, chat_history, vectorstore, llm, chatgpt_enabled=True):
    """
    Main function to get answers from our RAG system.
    Can operate in two modes:
    1. RAG + LLM: Uses both document knowledge and ChatGPT
    2. RAG Only: Uses only document knowledge
    
    Args:
        query (str): The user's question
        chat_history (list): List of (human, ai) message tuples
        vectorstore: The vector store for document retrieval
        llm: The language model to use
        chatgpt_enabled (bool): Whether to use ChatGPT knowledge
        
    Returns:
        tuple: (answer, updated_history)
    """
    if vectorstore is None:
        logging.error("get_answer called with no vectorstore.")
        return "Error: Vector store not loaded. Please index documents first.", chat_history

    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    if chatgpt_enabled:
        # --- RAG + LLM Mode (Conversational) ---
        logging.info("Processing query in RAG+LLM mode.")
        
        # Set up conversation memory
        memory = ConversationBufferMemory(
            memory_key='chat_history', 
            input_key='question',
            output_key='answer', 
            return_messages=True
        )
        
        # Add previous messages to memory
        for human_msg, ai_msg in chat_history:
            memory.chat_memory.add_user_message(human_msg)
            memory.chat_memory.add_ai_message(ai_msg)

        # Create the conversation chain
        conv_chain = ConversationalRetrievalChain.from_llm(
            llm=llm, 
            retriever=retriever, 
            memory=memory,
            return_source_documents=False,
            condense_question_prompt=CONDENSE_QUESTION_PROMPT,
            combine_docs_chain_kwargs={"prompt": ANSWER_PROMPT},
            verbose=False
        )
        
        try:
            # Get the answer
            result = conv_chain.invoke({"question": query})
            answer = result.get('answer', "Sorry, I encountered an issue processing the answer.")
            updated_history = chat_history + [(query, answer)]
            logging.info("RAG+LLM query processed successfully.")
            return answer, updated_history
        except Exception as e:
            logging.error(f"Error in conversational chain: {e}", exc_info=True)
            return f"Error in RAG+LLM mode: {e}", chat_history

    else:
        # --- RAG Only Mode (Strict) ---
        logging.info("Processing query in RAG-only mode.")
        
        try:
            # Create and run the RAG-only chain
            rag_chain = create_rag_only_chain(vectorstore, llm)
            
            if rag_chain is None:
                return "Error: Failed to create RAG-only chain.", chat_history
            
            answer = rag_chain.invoke(query)
            updated_history = chat_history + [(query, answer)]
            logging.info("RAG-only query processed successfully.")
            return answer, updated_history
        except Exception as e:
            logging.error(f"Error in RAG-only chain: {e}", exc_info=True)
            return f"Error in RAG-only mode: {e}", chat_history

def get_streaming_answer(query, chat_history, vectorstore, llm, chatgpt_enabled=True):
    """
    Streaming version of get_answer function that yields chunks of the response as they're generated.
    This allows for a more interactive chat experience.
    
    Args:
        query (str): The user's question
        chat_history (list): List of (human, ai) message tuples
        vectorstore: The vector store for document retrieval
        llm: The language model to use
        chatgpt_enabled (bool): Whether to use ChatGPT knowledge
        
    Yields:
        str: Chunks of the response
    """
    if vectorstore is None:
        yield "Error: Vector store not loaded. Please index documents first."
        return

    # Create streaming-enabled LLM
    streaming_llm = llm
    
    if not streaming_llm.streaming:
        logging.warning("get_streaming_answer was called with a non-streaming LLM. Response will not stream properly.")
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    if chatgpt_enabled:
        # --- RAG + LLM Mode (Conversational) with streaming ---
        logging.info("Processing streaming query in RAG+LLM mode.")
        
        # Set up conversation memory
        memory = ConversationBufferMemory(
            memory_key='chat_history', 
            input_key='question',
            output_key='answer', 
            return_messages=True
        )
        
        # Add previous messages to memory
        for human_msg, ai_msg in chat_history:
            memory.chat_memory.add_user_message(human_msg)
            memory.chat_memory.add_ai_message(ai_msg)
        
        try:
            # First, get the standalone question
            if chat_history:
                standalone_chain = (
                    {"question": RunnablePassthrough(), "chat_history": lambda _: get_buffer_string(memory.chat_memory.messages)}
                    | CONDENSE_QUESTION_PROMPT
                    | llm
                    | StrOutputParser()
                )
                standalone_question = standalone_chain.invoke(query)
                logging.info(f"Standalone question: {standalone_question}")
            else:
                standalone_question = query
            
            # Retrieve relevant documents
            docs = retriever.get_relevant_documents(standalone_question)
            context = "\n\n".join(doc.page_content for doc in docs)
            
            # Format the prompt with context and chat history
            formatted_prompt = ANSWER_PROMPT.format(
                context=context,
                chat_history=get_buffer_string(memory.chat_memory.messages),
                question=standalone_question
            )
            
            # Stream tokens using the stream method
            for chunk in streaming_llm.stream(formatted_prompt):
                if hasattr(chunk, 'content'):
                    yield chunk.content
                else:
                    yield str(chunk)
                
        except Exception as e:
            logging.error(f"Error in streaming RAG+LLM: {e}", exc_info=True)
            yield f"Error in streaming RAG+LLM mode: {e}"
    
    else:
        # --- RAG Only Mode (Strict) with streaming ---
        logging.info("Processing streaming query in RAG-only mode.")
        
        try:
            # Retrieve relevant documents
            docs = retriever.get_relevant_documents(query)
            if not docs:
                yield "No relevant documents found for your query. Try rephrasing or enabling ChatGPT Knowledge mode."
                return
                
            context = "\n\n".join(doc.page_content for doc in docs)
            
            # Format the prompt with context
            formatted_prompt = RAG_ONLY_ANSWER_PROMPT.format(
                context=context,
                question=query
            )
            
            # Stream tokens
            for chunk in streaming_llm.stream(formatted_prompt):
                if hasattr(chunk, 'content'):
                    yield chunk.content
                else:
                    yield str(chunk)
                
        except Exception as e:
            logging.error(f"Error in streaming RAG-only mode: {e}", exc_info=True)
            yield f"Error in streaming RAG-only mode: {e}" 