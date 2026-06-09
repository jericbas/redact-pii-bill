import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import io
import os

# Configuration: You might need to point this to your Tesseract executable path
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

def extract_text_from_image(image_bytes: bytes) -> str:
    """Extracts text from image bytes using Tesseract OCR."""
    image = Image.open(io.BytesIO(image_bytes))
    text = pytesseract.image_to_string(image)
    return text

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extracts text from PDF bytes by converting pages to images."""
    images = convert_from_bytes(pdf_bytes)
    full_text = ""
    for image in images:
        full_text += pytesseract.image_to_string(image)
    return full_text

def extract_text_from_file(file_path: str) -> str:
    """Helper to extract text from a file path."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.png', '.jpg', '.jpeg', '.bmp']:
        with open(file_path, 'rb') as f:
            return extract_text_from_image(f.read())
    elif ext == '.pdf':
        with open(file_path, 'rb') as f:
            return extract_text_from_pdf(f.read())
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
