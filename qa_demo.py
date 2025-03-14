"""
qa_demo.py

This script demonstrates the document question-answering capabilities.
It process a document and then answers questions about its content.
"""

import os
from pathlib import Path
import logging
from src.data_processing.document_processor import DocumentProcessor
from src.ml_models.document_qa import DocumentQA

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def run_qa_demo():
    """
    Run a demonstration of document QA capabilities.
    """

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        api_key = input("Please enter your OpenAI API key:")
        os.environ["OPENAI_API_KEY"] = api_key
    
    # Initialize our document processor
    processor = DocumentProcessor("test_documents", "processed_documents")

    # Process document
    doc_path = Path("test_documents/The Immutability of God.pdf")

    print(f"\nProcessing document: {doc_path.name}...")
    doc_result = processor.process_single_document(doc_path)
    print(f"Document processed successfully. Word count {doc_result['analysis']['basic_features']['word_count']}")

    # Initialize our QA system
    