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

def test_processor_initilization(test_dirs):
    """
    Test the initialization of the DocumentProcessor class.
    """
    input_dir, output_dir = test_dirs
    processor = DocumentProcessor(input_directory=input_dir, output_directory=output_dir)
    assert processor.input_dir == input_dir
    assert processor.output_dir == output_dir
    assert processor.supported_formats == {'.pdf', '.png', '.jpg', '.jpeg', '.tiff'}

def test_document_metadata():
    """
    Test metadata extraction from a document.
    Metadata helps us track and manage our documents.
    """

    test_file = Path("test_doc.pdf")
    processor = DocumentProcessor(input_directory="input", output_directory="output")

    metadata = processor.get_document_metadata(test_file)

    assert isinstance(metadata, DocumentMetadata)
    assert metadata.filename == "test_doc.pdf"
    assert metadata.file_type == ".pdf"