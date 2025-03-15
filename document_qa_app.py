"""
document_qa_app.py

A streamlit web application that demonstrates our intellignet document
processing and question-answering capabilites.
"""

import streamlit as st
import os
import tempfile
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import time

from src.data_processing.document_processor import DocumentProcessor
from src.ml_models.document_qa import DocumentQA

# Page configuration
st.set_page_config(page_title="Document Intelligence System", layout="wide")

# Header
st.title("📄 Intelligent Document QA System")
st.markdown("""
This application demonstrates an advanced document processing system that can:
- Extract text from PDF and image documents
- Analyze document content and features
- Answer questions about document content
""")

# Sidebar for API key
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("OpenAI API key", type="password",
                            help="Enter your OpenAI API key to enable document processing")
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This system combines OCR, embeddings, and language models to create an intelligent document analysis tool.")
    st.markdown("Built by: Vitor C.")

# Main content
tab1, tab2 = st.tabs(["Document Analysis", "Question Answreing"])

# Initialize session state
if 'processed_document' not in st.session_state:
    st.session_state.processed_document = None
if 'qa_system' not in st.session_state:
    st.session_state.qa_system = None
if 'document_name' not in st.session_state:
    st.session_state.document_name = None

