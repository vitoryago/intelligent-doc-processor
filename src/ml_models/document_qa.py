"""
document_qa.py

This module adds document question-answering capabilities using LangChain.
It creates a system that can answer specific questions about documents
by understanding their content and retrieving relevant information.
"""

import os
from typing import Dict, List, Optional
import logging
from pathlib import Path
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import retrieval_qa
from langchain.prompts import PromptTemplate

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
