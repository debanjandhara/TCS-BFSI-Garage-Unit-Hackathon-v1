# RAG Chatbot

A Retrieval Augmented Generation (RAG) chatbot that allows you to chat with your documents.

## Features

- Upload and index documents (PDF, TXT, CSV, XLSX, DOCX, JSON)
- Chat with your documents using natural language
- Two operation modes:
  - RAG + LLM: Uses both document knowledge and ChatGPT's general knowledge
  - RAG Only: Strictly uses only information found in your documents
- Multiple chat sessions with history
- Document management
- Streaming responses
- Conversation editing and retry

## Project Structure

```
/
│
├── app/                        # Main application folder
│   ├── main.py                 # Main entry point for the app (Streamlit)
│   │
│   ├── core/                   # Core functionality
│   │   ├── rag_engine.py       # Core RAG implementation
│   │   ├── llm.py              # LLM and embedding models
│   │   ├── document_store.py   # Document loading and processing
│   │   └── vector_store.py     # Vector store functionality
│   │
│   ├── ui/                     # User interface components
│   │   ├── sidebar.py          # Sidebar UI components
│   │   └── chat.py             # Chat interface components
│   │
│   ├── utils/                  # Utility functions
│   │   ├── config.py           # Configuration handling
│   │   ├── logging_utils.py    # Logging utilities
│   │   └── session.py          # Session state management
│   │
│   └── config/                 # Configuration files
│       └── prompts.py          # Prompt templates
│
├── data/                       # Where documents are stored
├── vectorstore/                # Vector database storage
├── logs/                       # Log files
├── run.py                      # Launcher script
├── .env-example                # Example environment variables
└── requirements.txt            # Project dependencies
```

## Prerequisites

- Python 3.8 or later
- An OpenAI API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/rag-chatbot.git
   cd rag-chatbot
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Run the application:
   ```
   python run.py
   ```
   
   Alternatively, you can run Streamlit directly:
   ```
   streamlit run app.py
   ```

2. The application will open in your default web browser.

3. Enter your OpenAI API key if not already in the `.env` file.

4. Upload documents using the sidebar.

5. Click "Index Uploaded Documents" to process and vectorize your documents.

6. Start chatting with your documents!

## Configuration

You can configure the application by setting these environment variables in a `.env` file:

- `OPENAI_API_KEY`: Your OpenAI API key
- `LLM_MODEL`: The LLM model to use (default: "gpt-4o-mini")
- `EMBEDDING_MODEL`: The embedding model to use (default: "text-embedding-3-small")
- `DATA_PATH`: Path to store uploaded documents (default: "data/")
- `VECTORSTORE_PATH`: Path to store the vector database (default: "vectorstore/db_faiss")
- `LOGS_PATH`: Path to store log files (default: "logs/")

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [LangChain](https://www.langchain.com/)
- UI powered by [Streamlit](https://streamlit.io/)
- Vector search by [FAISS](https://github.com/facebookresearch/faiss)