"""
document_processor.py
Core module for intelligent document processing.

This module handles the main document processing pipeline, including:
- Document validation and loading
- Text extraction
- Initial classification
- Information extraction
"""

import os
from pathlib import Path
from typing import List, Dict, Union, Optional
from dataclasses import dataclass
import logging

# Set up logging to help us track what's happening in our processor
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DocumentMetadata:
    """
    Stores metadata about processor documents.
    Using a dataclass makes our data structure clear and maintanable
    """
    filename: str
    file_type: str
    size: int
    page_count: Optional[int] = None
    processing_status: str = "pending"

class DocumentProcessor:
    """
    Main document processing class that orchestrates the entire pipeline.
    """

    def __init__(self, input_directory: Union[str, Path], output_directory: Union[str, Path]):
        """
        Initialize the processor with input and output directories.

        Args:
            input_directory (Union[str, Path]): The directory to read documents from.
            output_directory (Union[str, Path]): The directory to write processed documents to.
        """

        self.input_dir = Path(input_directory)
        self.output_dir = Path(output_directory)
        self.supported_formats = {'.pdf', '.png', '.jpg', '.jpeg', '.tiff'}

        # Create the output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Initialized DocumentProcessor with input directory: {self.input_dir} and output directory: {self.output_dir}")

    def get_document_metadata(self, file_path: Path) -> DocumentMetadata:
        """
        Extracts basic metadata from a document file.
        """
        return DocumentMetadata(
            filename=file_path.name,
            file_type=file_path.suffix,
            size=file_path.stat().st_size,
            processing_status="initialized"
        )
    
    def process_single_document(self, file_path: Union[str, Path]) -> Dict:
        """
        Process single document through our pipeline.

        This method orchestrates the document processing workflow:
        1. Validate the document
        2. Extract metadata
        3. Prepare for processing
        4. Extract text and information
        5. Save results
        """

        file_path = Path(file_path)

        if file_path.suffix.lower() not in self.supported_formats:
            raise ValueError(f"Unsupported format: {file_path.suffix}. Supported formats: {self.supported_formats}")
        
        metadata = self.get_document_metadata(file_path)
        logger.info(f"Processing document: {metadata.filename}")

        try:
            result = {
                "metadata": metadata.__dict__,
                "status": "success",
                "message": "Document processed successfully"
            }

            return result
        
        except Exception as e:
            logger.error(f"Error processing document {file_path}: {e}")
            raise
        