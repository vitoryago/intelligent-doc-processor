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
    qa_system = DocumentQA(api_key=api_key)
     # Load the document content
    print("\nPreparing document for question answering...")
    qa_result = qa_system.load_document(doc_result["content"], doc_path.stem)
    print(f"Document prepared with {qa_result['chunks']} chunks")
    
    # Define some sample questions
    questions = [
        "What is the main topic of this document?",
        "What does immutability mean according to this text?",
        "Why is God's immutability important according to the author?"
    ]
    
    # Answer each question
    print("\n=== Document Question-Answering Demo ===")
    for i, question in enumerate(questions, 1):
        print(f"\nQuestion {i}: {question}")
        print("Thinking...")
        answer = qa_system.ask(question)
        print(f"Answer: {answer['answer']}")

if __name__ == "__main__":
    run_qa_demo()