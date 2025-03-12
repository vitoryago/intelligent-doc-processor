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

