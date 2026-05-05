import fitz  # PyMuPDF
from paddleocr import PaddleOCR
import cv2
import numpy as np

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text()

    return text


def process_pdf(pdf_path):
    print(f"Processing: {pdf_path}")

    text = extract_text_from_pdf(pdf_path)

    # If very little text → likely scanned
    if len(text.strip()) < 100:
        print("⚠️ Low text detected -> Possibly scanned PDF")

        ocr_text = extract_text_with_ocr(pdf_path)

        if ocr_text.strip():
            print("✅ OCR text extracted successfully")
            return ocr_text
        else:
            print("❌ OCR also failed")
            return None

    print("✅ Text successfully extracted")
    return text

def extract_text_with_ocr(pdf_path):
    print("⚠️ Using PaddleOCR for scanned PDF...")

    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    doc = fitz.open(pdf_path)

    full_text = ""

    for page_num in range(len(doc)):
        page = doc[page_num]

        # Convert PDF page to image
        pix = page.get_pixmap()
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, -1)

        # Run OCR
        result = ocr.ocr(img)

        if result[0]:
            for line in result[0]:
                text = line[1][0]
                confidence = line[1][1]
                full_text += text + "\n"

    return full_text