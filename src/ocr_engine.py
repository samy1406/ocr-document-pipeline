import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # ← here
from pdf2image import convert_from_path

def image_to_text(image):
    text = pytesseract.image_to_string(image, config='--psm 6')
    return text

def image_to_data(image):
    df = pytesseract.image_to_data(image, output_type=pytesseract.Output.DATAFRAME)
    df = df[(df['conf'] != -1) & (df['conf'] > 60)]
    return df

def pdf_to_text(pdf_path):
    pages = convert_from_path(pdf_path, dpi=300)
    
    text_pages = []

    for page in pages:
        page_text = image_to_text(page)
        text_pages.append(page_text)
    
    return "\n\n".join(text_pages)