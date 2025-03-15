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
