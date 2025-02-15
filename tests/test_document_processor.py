"""
test_document_processor.py
Tests for our document processing system.

These tests help ensure our code works correctly and catch any issues
before they affect our users.
"""

import pytest
from pathlib import Path
from src.data_processing.document_processor import DocumentProcessor

@pytest.fixture
def test_dirs(tmp_path):
    """
    Creates temporary directories for testing.
    tmp_path is a pytest fixture that provides a temporary directory.
    """
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()
    return input_dir, output_dir

@pytest.fixture
def sample_document(tmp_path):
    """
    Creates a temporary test document.
    This is like creating a practice document that we can use for testing.
    """

    doc_path = tmp_path / "test_doc.pdf"
    doc_path.write_text("This is a test document.")
    return doc_path

def test_processor_initialization(test_dirs):
    """
    Test that our DocumentProcessor starts up correctly.
    This is like checking if a machine turns on properly before using it.
    """
    # Get our temporary directories from the fixture
    input_dir, output_dir = test_dirs
    
    # Create a new DocumentProcessor
    processor = DocumentProcessor(input_directory=input_dir, output_directory=output_dir)
    
    # Now we use 'assert' to check if things are working correctly
    # Think of assert like saying "Make sure this is true"
    assert processor.input_dir == input_dir  # Check if input directory is set correctly
    assert processor.output_dir.exists()     # Check if output directory exists
    assert processor.supported_formats == {'.pdf', '.png', '.jpg', '.jpeg', '.tiff'}

def test_document_metadata(sample_document):
    """
    Test that we can correctly get information about a document.
    This is like checking if we can read the basic details of a document correctly.
    """
    # Create a processor for testing
    processor = DocumentProcessor(input_directory="input", output_directory="output")
    
    # Get metadata from our test document
    metadata = processor.get_document_metadata(sample_document)
    
    # Check if the metadata is correct
    # Each assert is like a checkpoint that verifies something specific
    assert metadata.filename == "test_doc.pdf"  # Check if filename is correct
    assert metadata.file_type == ".pdf"         # Check if file type is correct
    assert metadata.processing_status == "initialized"  # Check if status is correct
    assert metadata.size > 0  # Check if we got a valid file size

def test_invalid_document():
    """
    Test how our processor handles invalid documents.
    This is like checking if our system properly handles mistakes.
    """
    processor = DocumentProcessor(input_directory="input", output_directory="output")
    
    # Try to process a non-existent file
    with pytest.raises(ValueError):  # This tells pytest we expect an error
        processor.process_single_document("nonexistent.xyz")