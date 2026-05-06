import preprocessor
import ocr_engine
import postprocessor

def postprocess_text(text):
    cleaned = postprocessor.clean_text(text)
    
    return {
        "date": postprocessor.extract_date(cleaned),
        "address": postprocessor.extract_address(cleaned),
        "products": postprocessor.extract_product_names(cleaned),
        "descriptions": postprocessor.extract_line_item_descriptions(cleaned),
        "prices": postprocessor.extract_prices(cleaned)
    }

def process_document(file_path):
    if file_path.lower().endswith(".pdf"):
        ocr_text = ocr_engine.pdf_to_text(file_path)
        
        text = postprocess_text(ocr_text)
    else:
        # If it's a single image, we wrap it in a list to keep the loop consistent
        fixed_image = preprocessor.preprocess_image(file_path)
        ocr_text = ocr_engine.image_to_text(fixed_image)
        # print("RAW TEXT:", ocr_text[:500])
        text = postprocess_text(ocr_text)
    
    return text

if __name__ == "__main__":
    import sys
    result = process_document(sys.argv[1])
    print(result)