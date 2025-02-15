"""
process_test_documents.py

This script demonstrates how our document processor works with real documents.
It shows how to:
1. Set up the processor
2. Process different types of documents
3. Handle any erros that might occur
4. Display the results in a readable way
"""

import os
from pathlib import Path
from src.data_processing.document_processor import DocumentProcessor
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_documents_in_folder(input_folder: str, output_folder: str):
    """
    Processes all supported documents in a folder.

    This function acts like an office worker going through a folder of documents:
    1. Looks at each document in the input folder
    2. Decides if it can process that type of document
    3. Processes each valid document
    4. Saves the results in the output folder
    5. Keeps track of any problemes that occur
    """

    # Create a DocumentProcessor instance
    processor = DocumentProcessor(input_directory=input_folder, output_directory=output_folder)

    # Get all files in the input folder
    input_path = Path(input_folder)

    # Keep track of our success and failures
    processed_files = []
    failed_files = []

    # Process each file in the input folder
    for file_path in input_path.iterdir():
        if file_path.is_file():
            try:
                logger.info(f"Attempting to process file: {file_path.name}")
                
                # Process the document
                result = processor.process_single_document(file_path)

                # Save the results
                output_file = Path(output_folder) / f"{file_path.stem}_processed.txt"
                with open(output_file, "w", encoding="utf-8") as f:
                    # Write the metadata
                    f.write(f"=== Document Analysis Result ===\n")
                    f.write(f"FileName: {result['metadata']['filename']}\n")
                    f.write(f"File Type: {result['metadata']['file_type']}\n")
                    f.write(f"Size: {result['metadata']['size']} bytes\n")
                    f.write(f"Status: {result['metadata']['processing_status']}\n\n")

                    # Write extracted text
                    f.write(f"=== Extracted Text ===\n")
                    f.write(result['content'])
                
                processed_files.append(file_path.name)
                logger.info(f"Document processed successfully: {file_path.name}")
            
            except Exception as e:
                logger.error(f"Error processing document: {str(e)}")
                failed_files.append((file_path.name, str(e)))
            
            # Print a summary of what happened
            print("\n=== Processing Summary ===")
            print(f"Successfully processed: {len(processed_files)} files:")
            for filename in processed_files:
                print(f"  ✓ {filename}")

            if failed_files:
                print(f"\nFailed to process: {len(failed_files)} files:")
                for filename, error in failed_files:
                    print(f"  ✗ {filename}: {error}")

if __name__ == "__main__":
    # Define our input and output folders
    input_folder = "test_documents"
    output_folder = "processed_documents"

    # Create the input folder if it doesn't exist
    Path(input_folder).mkdir(parents=True, exist_ok=True)

    # Process all documents
    process_documents_in_folder(input_folder=input_folder, output_folder=output_folder)
    
