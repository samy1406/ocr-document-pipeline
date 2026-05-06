import re

def clean_text(text):
    """
    Cleans OCR artifacts (extra whitespace, special chars) 
    to make regex matching more reliable.
    """

    if not text:
        return ""
    
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s.,$%-]', '', text)
    return text.strip()

def extract_date(text):
    """
    re.search: Finds the first occurrence of a date pattern 
    (e.g., DD/MM/YYYY or Month DD, YYYY).
    """
    date_pattern = r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4})'
    
    match = re.search(date_pattern, text, re.IGNORECASE)

    if match:
        return match.group().strip()
    
    return None

def extract_address(text):
    """
    re.search: Looks for the specific block of text containing 
    city, state, and zip code to locate the vendor/client address.
    """
    address_pattern = r'[A-Z][a-z]+,?\s[A-Z]{2}\s\d{5}'
    match = re.search(address_pattern, text)
    return match.group().strip() if match else None
    

def extract_product_names(text):
    """
    re.findall: Scans the text for multiple product/service identifiers, 
    often found at the start of line items.
    """
    product_pattern = r'(?:Item|Product):\s?([A-Za-z0-9\s-]+)'
    return re.findall(product_pattern, text)

def extract_line_item_descriptions(text):
    """
    re.findall: Captures the descriptive text associated with 
    each charged item.
    """
    description_pattern = r'([A-Za-z\s]{5,30})(?=\s?\$?\d+\.\d{2})'
    
    matches = re.findall(description_pattern, text)
    
    # Clean up results (remove extra spaces)
    return [item.strip() for item in matches if item.strip()]

def extract_prices(text):
    """
    re.findall: Finds all currency-formatted numbers (e.g., $XX.XX) 
    to capture individual item costs and the total.
    """
    price_pattern = r'\$?\s?[\d,]+\.\d{2}'
    return re.findall(price_pattern, text)

    
