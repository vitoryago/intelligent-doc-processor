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
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from src.ml_models.text_analyzer import DocumentAnalyzer
import sys

# Set up paths with your specific Poppler location
POPPLER_PATH = r"C:\Program Files\Poppler\Release-24.08.0-0\poppler-24.08.0\Library\bin"
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Set up logging to help us track what's happening in our processor
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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
    text_content: str = ""

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
    
    def _extract_text_from_image(self, image: Image.Image):
        """
        Helper method to extract text from a single image using OCR.
        This is like reading text from a photograph or scanned document.
        """

        try:
            # Use pytesseract to extract text from the image
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from image: {str(e)}")
            raise
    
    def _extract_text_from_pdf(self, file_path: Path) -> str:
        """
        Helper method to extract text from PDF files.
        """
        try:
            # Convert PDF to images using explicit poppler path
            pages = convert_from_path(
                file_path,
                poppler_path=POPPLER_PATH  # Using our defined Poppler path
            )
            
            # Extract text from each page
            text_content = []
            for page_num, page in enumerate(pages, 1):
                logger.info(f"Processing page {page_num} of {file_path.name}")
                text = pytesseract.image_to_string(page)
                text_content.append(text.strip())

            # Join all the text together with page breaks
            return "\n\n".join(text_content)
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise
    
    def extract_text_from_document(self, file_path: Path) -> str:
        """
        Extract text content from a document file.
        This method figures out what kind of document we have and processes it accordingly.
        """
        try:
            if file_path.suffix.lower() == ".pdf":
                logger.info(f"Processing PDF document: {file_path.name}")
                return self._extract_text_from_pdf(file_path)
            elif file_path.suffix.lower() in {".png", ".jpg", ".jpeg", ".tiff"}:
                logger.info(f"Processing image document: {file_path.name}")
                with Image.open(file_path) as img:
                    return self._extract_text_from_image(img)
        except Exception as e:
            logger.error(f"Error extracting text from document: {str(e)}")
            raise
    
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

            # Extract texto from the document
            extracted_text = self.extract_text_from_document(file_path)
            
            # Perform ML analysis
            analyzer = DocumentAnalyzer()
            analysis_results = analyzer.analyze_document(extracted_text)

            # Prepare the results
            result = {
                "metadata": metadata.__dict__,
                "content": extracted_text,
                "analysis": analysis_results,
                "status": "success",
                "message": "Document processed successfully"
            }

            return result
        
        except Exception as e:
            logger.error(f"Error processing document {file_path}: {str(e)}")
            metadata.processing_status = "failed"
            raise