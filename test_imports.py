# test_imports.py
print("Testing imports...")

try:
    import pytesseract
    print("✓ pytesseract imported successfully")
except ImportError as e:
    print("✗ pytesseract import failed:", e)

try:
    from pdf2image import convert_from_path
    print("✓ pdf2image imported successfully")
except ImportError as e:
    print("✗ pdf2image import failed:", e)

try:
    from PIL import Image
    print("✓ Pillow imported successfully")
except ImportError as e:
    print("✗ Pillow import failed:", e)

print("\nAll import tests completed!")