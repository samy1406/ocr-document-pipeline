import re

def clean_text(text):
    if not text:
        return ""
    # We keep commas and dots now as they are critical for European price formats
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s.,$%-/]', '', text)
    return text.strip()

def extract_date(text):
    # FIX: Use word boundaries (\b) to ensure we don't grab part of a longer Tax ID.
    # Also specifically looking for / or - separators for the numeric version.
    date_pattern = r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4})\b'
    match = re.search(date_pattern, text, re.IGNORECASE)
    return match.group().strip() if match else None

def extract_prices(text):
    # FIX: Changed \. to [.,] to support both $1,299.00 and 209,00 formats.
    price_pattern = r'\$?\s?\b\d+[\.,]\d{2}\b'
    return re.findall(price_pattern, text)

def extract_product_names(text):
    # FIX: Instead of looking for "Item:", we look for numbered lines (e.g., "1. Widget")
    # Pattern: Digit + dot + space + Word
    product_pattern = r'\b(\d{1,2})\.?\s+([A-Z][A-Za-z0-9\s!]{3,40}?)(?=\s+\d+,\d{2})'
    return re.findall(product_pattern, text)

def extract_line_item_descriptions(text):
    # FIX: Updated the lookahead to support the new price format [.,]
    description_pattern = r'([A-Za-z\s]{5,30})(?=\s?\$?\d+[\.,]\d{2})'
    matches = re.findall(description_pattern, text)
    return [item.strip() for item in matches if item.strip()]

def extract_address(text):
    # This remains an "anchor." To get the street, you'd usually look 
    # for the 20-30 characters preceding this match.
    address_pattern = r'[A-Z][a-z]+,?\s[A-Z]{2}\s\d{5}'
    match = re.search(address_pattern, text)
    return match.group().strip() if match else None