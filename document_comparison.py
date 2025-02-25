"""
document_comparison.py
Script to compare and analyze our different document types
"""

from pathlib import Path
from src.data_processing.document_processor import DocumentProcessor
from src.ml_models.text_analyzer import DocumentAnalyzer
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def compare_documents():
    """
    Analyzes and compares the documents in our test folder,
    generating visualizations and insights about their differences.
    """
    logger.info("Starting document comparison analysis")
    
    # Initialize our processor
    processor = DocumentProcessor("test_documents", "processed_documents")
    
    # Get the paths to our test documents
    job_desc_path = Path("test_documents/Analytics Engineer - Marketing.pdf")
    theology_doc_path = Path("test_documents/The Immutability of God.pdf")
    
    # Process both documents
    logger.info(f"Processing document: {job_desc_path.name}")
    job_desc = processor.process_single_document(job_desc_path)
    
    logger.info(f"Processing document: {theology_doc_path.name}")
    theology_doc = processor.process_single_document(theology_doc_path)
    
    # Create analyzer and compare documents
    logger.info("Comparing documents...")
    analyzer = DocumentAnalyzer()
    comparison = analyzer.compare_documents(
        job_desc['content'],
        theology_doc['content'],
        "Job Description",
        "Theological Text"
    )
    
    # Print the results
    print("\n=== Document Comparison Results ===")
    for doc_name, doc_info in comparison['document_comparison'].items():
        print(f"\n{doc_name}:")
        print("  Top words:")
        for word, count in doc_info['top_words']:
            print(f"    - {word}: {count} times")
        
        print("\n  Document Features:")
        for feature, value in doc_info['features'].items():
            if isinstance(value, float):
                print(f"    - {feature}: {value:.2f}")
            else:
                print(f"    - {feature}: {value}")
    
    logger.info("Document comparison complete")
    print("\nVisualizations have been saved as 'word_importance.png' and 'feature_comparison.png'")

if __name__ == "__main__":
    compare_documents()