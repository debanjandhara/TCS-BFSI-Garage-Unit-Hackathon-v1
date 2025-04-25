"""
Launcher script for the RAG Chatbot application
"""

import subprocess
import os
import sys

def main():
    """
    Launch the Streamlit application
    """
    print("Starting RAG Chatbot...")
    
    try:
        # Get the path to the Streamlit executable
        streamlit_path = os.path.join(os.path.dirname(sys.executable), "streamlit")
        
        # Launch the application with Streamlit
        subprocess.run([streamlit_path, "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\nStopping RAG Chatbot...")
    except Exception as e:
        print(f"Error launching application: {e}")
        print("\nTry running directly with: streamlit run app.py")

if __name__ == "__main__":
    main() 