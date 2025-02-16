
import pytesseract
import sys
import os

def check_tesseract():
    print("Checking Tesseract configuration...")

    # Print Python Version
    print(f"Python Version: {sys.version}")

    # Print Tesseract Version
    tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    print(f"Looking for Tesseract at: {tesseract_path}")
    print(f"File exists: {os.path.exists(tesseract_path)}")

    pytesseract.pytesseract.tesseract_cmd = tesseract_path

    try:
        # Try to get Tesseract version through Python
        version = pytesseract.get_tesseract_version()
        print(f"Tesseract Version: {version}")
        return True
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    check_tesseract()