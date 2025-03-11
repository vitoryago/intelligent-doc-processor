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

class DocumentQA:
    """
    A system that can answer questions about documents by understanding their content.

    This class:
    1. Splits documents into manageable chunks
    2. Creates vector embeddings for efficient retrievel
    3. Uses language model to generate answers based on relevant contexts.
    """
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the document QA system.

        Args:
            api_key: OpenAI API key (optional if already set as environment variable)
        """

        # Set API key if provided
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        elif not os.environ.get("OPENAI_API_KEY"):
            raise ValueError("OpenAI API key is required either as parameter or environment variable")
        
        # Initialize the language model
        self.llm = ChatOpenAI(
            model_name = "gpt-3.5-turbo",
            temperature=0 # Use 0 for more factual, deterministic responses
        )

        # Initialize the text splitter for breaking documents into chunks
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunck_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )

        # Initialize the embeddings model
        self.embeddings = OpenAIEmbeddings()

        # We'll create these per document
        self.vectorstore = None
        self.qa_chain = None

        logger.info("DocumentQA system initialized")
    
    def load_documents(self, text: str, document_name: str = "document") -> Dict:
        """
        Process a document for question answering

        Args:
            text: The document text content
            document_name: A name to identify this document
        Returns:
            Information about the loaded document
        """

        logger.info(f"Loading document: {document_name}")

        # Split the document into chunks
        chunks = self.text_splitter.split_text(text)
        chunk_count = len(chunks)
        logger.info(f"Documento split into {chunk_count} chunks")

        # Create metadata for each chunk to track its source
        metadatas = [{"source": f"{document_name}", "chunk": i} for i in range(chunk_count)]

        # Create a vector store from the chunks
        self.vectorstore = FAISS.from_texts(
            texts=chunks,
            embedding=self.embeddings,
            metadatas=metadatas
        )

        # Create a costum prompt template that instructs the model how to answer
        qa_template = """
        You are an intelligent document analysis assistant. You answer questions based on the provided context from a document.

        Context information is below:
        ------------------------------
        {context}
        ------------------------------

        Given the context information and not prior knowledge, answer the question {question}

        If the answer cannot be determined from the context, say "I cannot answer this based on the provided document."
        """

        PROMPT = PromptTemplate(
            template=qa_template,
            input_variables=["context", "question"]
        )

        # Create the QA chain that will retrieve relevant chunks and generate answers
        self.qa_chain = retrieval_qa.from_chain_type()