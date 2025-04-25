# TCS-BFSI-Garage-Unit-Hackathon Project Report

## Project: AI-Powered Insurance Policy Information Chatbot

### Table of Contents
1. [Executive Summary](#executive-summary)
2. [Problem Statement](#problem-statement)
3. [Technical Approach](#technical-approach)
4. [Architecture](#architecture)
5. [Implementation Details](#implementation-details)
6. [Features Implemented](#features-implemented)
7. [Methodology](#methodology)
8. [Testing & Evaluation](#testing--evaluation)
9. [Results & Discussion](#results--discussion)
10. [Future Enhancements](#future-enhancements)
11. [Conclusion](#conclusion)

---

## Executive Summary

This report presents the development and implementation of an AI-powered Insurance Policy Information Chatbot built for the TCS-BFSI-Garage-Unit-Hackathon. The solution employs Retrieval Augmented Generation (RAG) technology to provide accurate, context-aware responses to customer inquiries about various insurance policies and procedures.

The chatbot leverages large language model (LLM) capabilities enhanced by a custom knowledge base created from insurance policy documents. It provides a user-friendly interface that allows customers to easily upload documents, ask questions, and receive accurate information specific to their insurance queries. The system demonstrates the practical application of advanced AI technologies to solve real business challenges in the insurance sector.

---

## Problem Statement

### Background
Insurance companies offer a variety of policies, including health, life, auto, and home insurance. Customers often have questions about the different types of policies, coverage options, premiums, and claim processes. Providing timely and accurate information is crucial for customer satisfaction and decision-making. An AI-powered chatbot can assist customers by answering their queries about insurance policies, helping them understand their options and make informed decisions.

### Objective
Develop a chatbot that can assist customers with queries related to different types of insurance policies offered by the company. The chatbot should understand natural language, provide accurate responses, and guide customers through the information they need.

### Requirements
1. **LLM**: Use LLM for natural language processing
2. **Knowledge Base Integration**:
   - Create a knowledge base with information about different insurance policies, coverage options, premiums, and claim processes.
   - Details can be shared in the form of PDF to create the knowledge base.
   - Ensure the chatbot can retrieve and present relevant information from the knowledge base.
3. **Conversation Management**:
   - Implement fallback mechanisms to escalate complex issues to human agents if necessary.
4. **User Interface**:
   - Design a simple chatbot interface that can be integrated into the company's website or mobile app.
5. **Presentation**:
   - Prepare a comprehensive report detailing the methodology, results, and conclusions.
   - Explain why the implemented approach was selected.
   - Submit the recording of the demo with voice over of what has been achieved along with the code.

---

## Technical Approach

Our solution implements a Retrieval Augmented Generation (RAG) system that combines the power of Large Language Models (LLMs) with a vector database of insurance policy information. This approach was chosen for several key reasons:

1. **Accuracy and Relevance**: RAG systems provide more accurate and factual responses by retrieving relevant information from a trusted knowledge base before generating answers.

2. **Up-to-date Information**: The system can be updated with new insurance policy documents without retraining the underlying language model.

3. **Transparency and Trust**: The chatbot can cite specific policies and documents, increasing user trust in the information provided.

4. **Reduced Hallucination**: By grounding responses in actual documents, the RAG approach significantly reduces the risk of the LLM "hallucinating" incorrect information.

5. **Cost Efficiency**: The approach is more efficient than fine-tuning large models, as it only requires indexing new documents rather than retraining.

6. **Dual-mode Operation**: The system operates in two modes:
   - **RAG + LLM Mode**: Uses both document knowledge and the LLM's general knowledge
   - **RAG-Only Mode**: Strictly uses only information found in the documents (for regulated information)

---

## Architecture

The application follows a modular architecture designed for maintainability, scalability, and ease of extension:

```
/
│
├── app.py                     # Main entry point for the Streamlit app
├── app/                       # Main application folder
│   ├── main.py                # Main application logic
│   │
│   ├── core/                  # Core functionality
│   │   ├── rag_engine.py      # Core RAG implementation
│   │   ├── llm.py             # LLM and embedding models
│   │   ├── document_store.py  # Document loading and processing
│   │   └── vector_store.py    # Vector store functionality
│   │
│   ├── ui/                    # User interface components
│   │   ├── sidebar.py         # Sidebar UI components
│   │   ├── chat.py            # Chat interface components
│   │   └── document_management.py # Document management UI
│   │
│   ├── utils/                 # Utility functions
│   │   ├── config.py          # Configuration handling
│   │   ├── logging_utils.py   # Logging utilities
│   │   └── session.py         # Session state management
│   │
│   └── config/                # Configuration files
│       └── prompts.py         # Prompt templates
│
├── data/                      # Where insurance policy documents are stored
├── vectorstore/               # Vector database storage
├── logs/                      # Log files
└── run.py                     # Launcher script
```

---

## Implementation Details

### Core Technologies and Libraries

1. **LangChain**: Used as the framework for connecting the LLM with the document retrieval system
2. **OpenAI**: Provides the underlying language model capabilities through GPT models
3. **FAISS**: A vector database for efficient similarity search of embedded documents
4. **Streamlit**: Powers the user interface for a seamless web experience
5. **Unstructured**: Used for document parsing and extraction

### Key Components

1. **Document Processing Pipeline**:
   - Supports multiple document formats (PDF, TXT, CSV, XLSX, DOCX, JSON)
   - Automatically loads and processes documents from the data directory
   - Splits documents into chunks of optimal size for retrieval
   - Preserves document context during chunking

2. **Vector Store Implementation**:
   - Creates embeddings for document chunks using OpenAI's embedding models
   - Stores these embeddings in a FAISS index for efficient similarity search
   - Optimized for fast retrieval during query time

3. **RAG Engine**:
   - Two operational modes:
     - RAG + LLM: Combines retrieved information with general knowledge
     - RAG Only: Strict retrieval-only approach for regulatory compliance
   - Customized prompt templates to optimize response quality
   - Streaming response generation for immediate feedback

4. **Session Management**:
   - Multiple chat sessions for different topics
   - Persistent conversation history
   - Session renaming and management

---

## Features Implemented

The following features have been successfully implemented in the chatbot solution:

### Document Management
- **Document Upload**: Users can upload insurance policy documents in various formats (PDF, TXT, CSV, XLSX, DOCX, JSON)
- **Document Indexing**: Automatic processing and vectorization of uploaded documents
- **Document Management**: Interface for viewing, adding, and removing documents from the knowledge base

### Intelligent Querying
- **Natural Language Processing**: The system understands natural language questions about insurance policies
- **Context-Aware Responses**: Maintains conversation context for follow-up questions
- **Two Operation Modes**:
  - **Standard Mode (RAG + LLM)**: Combines knowledge base information with the LLM's general knowledge
  - **Strict Mode (RAG Only)**: Uses only information found in the knowledge base, ideal for compliance requirements

### User Experience
- **Multi-Session Support**: Multiple chat sessions for different insurance topics
- **Streaming Responses**: Real-time streaming of AI responses for better user experience
- **Session Management**: Create, rename, and delete chat sessions
- **Visual Indicators**: File type icons and status notifications

### Integration Features
- **API Key Management**: Secure handling of OpenAI API keys
- **Configuration Options**: Customizable settings for models and paths
- **Logging System**: Comprehensive logging for debugging and auditing
- **Error Handling**: Graceful management of errors with informative messages

### Insurance-Specific Features
- **Policy Information Retrieval**: Quick access to specific policy details
- **Coverage Explanation**: Clear explanations of coverage options
- **Premium Information**: Accurate information about premium calculations
- **Claims Process Guidance**: Step-by-step guidance on the claims process

---

## Methodology

### 1. Knowledge Base Creation

The chatbot's knowledge base is created through a systematic process:

1. **Document Collection**: Insurance policy documents are collected and organized
2. **Document Processing**:
   - Documents are loaded using specialized loaders for each format
   - Text is extracted and cleaned to remove irrelevant information
   - Documents are split into semantic chunks with appropriate overlap
3. **Embedding Generation**:
   - Each document chunk is converted into a vector embedding using OpenAI's embedding models
   - These embeddings capture the semantic meaning of the text
4. **Vector Database Creation**:
   - Embeddings are stored in a FAISS index for efficient similarity search
   - The database is persisted to disk for future use

### 2. Query Processing Pipeline

When a user asks a question about insurance policies:

1. **Query Understanding**:
   - The user's query is analyzed for intent and context
   - If it's a follow-up question, it's reformulated to be standalone
2. **Relevant Document Retrieval**:
   - The query is converted to an embedding vector
   - The vector database is searched for the most similar document chunks
   - Top relevant chunks are retrieved (typically 3-5 chunks)
3. **Context Construction**:
   - Retrieved document chunks are combined to form a context
   - Chat history is incorporated for conversational awareness
4. **Response Generation**:
   - A carefully crafted prompt template is populated with the context and query
   - The LLM generates a response grounded in the provided context
   - In RAG-Only mode, the LLM is explicitly instructed to use only the provided information
5. **Response Delivery**:
   - The response is streamed to the user in real-time
   - The conversation history is updated

### 3. Test and Refinement

The system underwent multiple iterations of testing and refinement:

1. **Prompt Engineering**: Various prompt formulations were tested to determine optimal response quality
2. **Chunking Strategy**: Different chunk sizes and overlap parameters were tested for retrieval accuracy
3. **Model Selection**: Different OpenAI models were evaluated for the best price-performance ratio
4. **UI/UX Testing**: The interface was refined based on user feedback

---

## Testing & Evaluation

### Testing Approach

The chatbot was tested comprehensively using:

1. **Unit Testing**: Individual components were tested in isolation
2. **Integration Testing**: Component interactions were verified
3. **End-to-End Testing**: Complete user flows were tested
4. **Performance Testing**: Response times and resource usage were measured

### Evaluation Metrics

The system was evaluated using:

1. **Response Accuracy**: Correctness of information provided
2. **Response Relevance**: How well responses addressed the specific question
3. **Response Completeness**: Whether all aspects of questions were addressed
4. **Response Time**: Speed of generating and displaying responses
5. **User Experience**: Ease of use and clarity of interface

### Test Results

The test results demonstrated:

- High accuracy when answering questions directly addressed in the knowledge base
- Appropriate indication when information was not found in the documents
- Reasonable response times (<2 seconds) for most queries
- Proper handling of document uploading and processing
- Seamless conversation flow and context maintenance

---

## Results & Discussion

### Key Achievements

1. **Accurate Information Retrieval**: The chatbot successfully retrieves specific insurance policy information with high accuracy.

2. **Natural Conversation Flow**: Users can ask follow-up questions without repeating context, creating a natural conversation experience.

3. **Document Management**: The system effectively processes and indexes various document formats containing insurance policy information.

4. **Dual Operation Modes**: The ability to switch between RAG+LLM and RAG-Only modes provides flexibility for different use cases.

5. **Seamless User Experience**: The Streamlit interface provides an intuitive, responsive user experience.

### Technical Innovations

1. **Prompt Engineering**: Custom-designed prompts that significantly improve the quality and relevance of responses.

2. **Session Management**: A flexible session system that allows users to maintain multiple separate conversations.

3. **Streaming Implementation**: Real-time response streaming that enhances the user experience.

4. **Modular Architecture**: Clean separation of concerns that allows for easy maintenance and extension.

### Integration with Insurance Domain

The system is particularly well-suited to the insurance domain due to:

1. **Document-Heavy Nature**: Insurance policies are typically documented in detail, making them ideal for RAG systems.

2. **Regulatory Compliance**: The RAG-Only mode ensures responses are strictly based on approved documents.

3. **Customer Self-Service**: Allows customers to get accurate policy information without contacting agents.

4. **Knowledge Consistency**: Ensures all customers receive the same accurate information about policies.

---

## Future Enhancements

Several potential enhancements could further improve the system:

1. **Multi-Modal Support**: Add support for images and diagrams within insurance documents.

2. **Personalized Responses**: Integrate with customer data to provide personalized policy information.

3. **Sentiment Analysis**: Detect customer frustration and escalate to human agents when needed.

4. **Advanced Analytics**: Track common questions to identify areas where policy documentation could be improved.

5. **Multi-Language Support**: Expand capabilities to handle questions in multiple languages.

6. **Voice Interface**: Add speech-to-text and text-to-speech capabilities for accessibility.

7. **Mobile Optimization**: Further optimize the interface for mobile devices.

8. **Enhanced Security**: Implement additional security measures for handling sensitive policy information.

---

## Conclusion

The AI-Powered Insurance Policy Information Chatbot represents a significant advancement in how insurance companies can provide information to their customers. By leveraging the latest in Retrieval Augmented Generation technology, the system delivers accurate, context-aware responses that help customers understand their insurance options.

The modular, well-structured architecture ensures the solution is maintainable and extensible, allowing for future enhancements as requirements evolve. The dual-mode operation provides flexibility for different use cases, from general information to strictly regulated content.

This project demonstrates that by combining cutting-edge LLM technology with a carefully designed retrieval system and user interface, we can create an effective solution that addresses real business needs in the insurance sector. The chatbot not only improves customer experience but also has the potential to reduce operational costs by automating routine information requests.

The solution developed for this hackathon is immediately applicable to real-world insurance scenarios and can be readily adapted to specific insurance companies by simply uploading their policy documents. No special formatting or preparation is required - the system works with standard document formats, making implementation straightforward for any insurance provider.

---

*This project was developed as part of the TCS-BFSI-Garage-Unit-Hackathon.* 