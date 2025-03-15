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

