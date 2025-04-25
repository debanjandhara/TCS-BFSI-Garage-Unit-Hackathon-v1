"""
Tests for the RAG engine
"""

import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the project root to the Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.rag_engine import create_rag_only_chain

class TestRagEngine(unittest.TestCase):
    """Tests for the RAG engine"""
    
    @patch('app.core.rag_engine.logging')
    def test_create_rag_only_chain_with_none_vectorstore(self, mock_logging):
        """Test create_rag_only_chain with None vectorstore"""
        # Arrange
        vectorstore = None
        llm = MagicMock()
        
        # Act
        result = create_rag_only_chain(vectorstore, llm)
        
        # Assert
        self.assertIsNone(result)
        mock_logging.error.assert_called_once_with("Vector store is None for RAG-only chain.")

if __name__ == '__main__':
    unittest.main() 