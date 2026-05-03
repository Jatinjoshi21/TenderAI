import re


def clean_text(text):
    if text is None:
        return None

    # 1. Normalize currency symbols
    text = text.replace("₹", "Rs")

    # 2. Fix common OCR mistakes
    text = text.replace("0", "0")  # keep zero
    text = text.replace("O", "0")  # O → 0 (only useful in numbers)

    # 3. Remove excessive spaces
    text = re.sub(r"\s+", " ", text)

    # 4. Fix line breaks (optional but helpful)
    text = text.replace("\n", " ")

    # 5. Remove weird characters
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    return text.strip()