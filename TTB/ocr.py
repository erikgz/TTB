import logging
import os
import re
import sys
import warnings

#os.environ['DISABLE_MODEL_SOURCE_CHECK'] = 'True'

#logging.getLogger('paddlex').setLevel(logging.WARNING) 
#logging.getLogger("ppocr").setLevel(logging.WARNING)
#logging.getLogger("ppocr").propagate = False


# Filter out the specific UserWarning regarding 'No ccache found'
warnings.filterwarnings(
    action='ignore',
    message="No ccache found. Please be aware that recompiling all source files may be required. You can download and install ccache from: https://github.com/ccache/ccache/blob/master/doc/INSTALL.md",
    category=UserWarning
)

from paddleocr import PaddleOCR


def ocr_paddle(label_file):
    paddle = PaddleOCR(use_textline_orientation=True, lang='en')
    result = paddle.predict(label_file)

    entry = result[0]
    texts = entry["rec_texts"]
    #scores = entry["rec_scores"]
    #text_to_score_dict = dict(list(zip(texts,scores)))
    return " ".join(texts)

def ocr_process_label(label_file, brand_name, product_class, volume_unit):
    label_text = ocr_paddle(label_file)

    print(f"label_text={label_text}")

    brand_match = re.search(r"\b(" + re.escape(brand_name) + r")\b", label_text, re.IGNORECASE)
    product_class_match = re.search(r"\b(" + re.escape(product_class) + r")\b", label_text, re.IGNORECASE)
    abv_match = re.search(r"(\d{1,3}\.?\d?)\s*(%|ALC\/VOL|ABV|PCT)", label_text, re.IGNORECASE)
    #volume_match = re.search(r"(\d+\.?\d*)\s*(mL|cL|dL|fl\s*oz|fl\.?\s*oz|L|oz|Litre)", label_text, re.IGNORECASE)
    volume_match = re.search(r"(\d+\.?\d*)\s*(" + re.escape(volume_unit) + ")", label_text, re.IGNORECASE)
    
    return {
        "brand": brand_match.group(1) if brand_match else None,
        "product_class": product_class_match.group(1) if product_class_match else None,
        "abv": abv_match.group(1) if abv_match else None,
        "volume": volume_match.group(1) if volume_match else None,
        "volume_unit": volume_match.group(2) if volume_match else None
    }


if __name__ == "__main__":
    params = len(sys.argv) - 1
    if params >= 1:
        label_file = sys.argv[1]
        if not os.path.exists(label_file) or not os.path.isfile(label_file):
            print(f"ERROR: {label_file} is not a valid file.")
            sys.exit(1)
        if params == 1:
            pass
        elif params == 4:
            brand_name = sys.argv[2]
            product_class = sys.argv[3]
            volume_unit = sys.arvg[4]
        else:
            print("ERROR: labe picture and optionally brand name and product class")
            sys.exit(1)
    else:
        print("ERROR: provide file with a label picture")
        sys.exit(1) 
        
    if params == 1:
        text = ocr_paddle(label_file);
        text_to_score_dict = ocr_paddle(label_file);
        print(f"========== OCR PADDLE ========== [{label_file}]")
        for text, prob in text_to_score_dict:
            print(f"Text: '{text:<30}' / Confidence: {prob:.2f} (0.0 to 1.0)")

        print("===============================")
    else:
        result = ocr_process_label(label_file, brand_name, product_class, volume_unit);
        print(f"========== OCR PROCESS LABEL ========== [{label_file}]")
        print(f"Result: '{result}'")

        print("===============================")
   
    
    sys.exit(0)