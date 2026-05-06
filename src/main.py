import preprocessor
import ocr_engine
import postprocess

def postprocess_text(text):
    cleaned = postprocess.clean_text(text)
    
    return {
        "date": postprocess.extract_date(cleaned),
        "address": postprocess.extract_address(cleaned),
        "products": postprocess.extract_product_names(cleaned),
        "descriptions": postprocess.extract_line_item_descriptions(cleaned),
        "prices": postprocess.extract_prices(cleaned)
    }

def process_document(file_path):
    if file_path.lower().endswith(".pdf"):
        ocr_text = ocr_engine.pdf_to_text(file_path)
        text = postprocess_text(ocr_text)
    else:
        # If it's a single image, we wrap it in a list to keep the loop consistent
        fixed_image = preprocessor.preprocess_image(file_path)
        ocr_text = ocr_engine.image_to_text(fixed_image)
        text = postprocess_text(ocr_text)
    
    return text

if __name__ == "__main__":
    import sys
    result = process_document(sys.argv[1])
    print(result)