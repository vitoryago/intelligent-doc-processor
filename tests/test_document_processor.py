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
