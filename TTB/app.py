import os
os.environ['DISABLE_MODEL_SOURCE_CHECK'] = 'True'

from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename

from .ocr import ocr_process_label

app = Flask(__name__)
# Configure an upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Set max content length to 16MB for safety
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

# Create the upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    """Renders the HTML form page."""
    return render_template('form.html')

@app.route('/submit_details', methods=['POST'])
def submit_details():
    """POST request with form data and label image to match. Returns JSON with results."""
    
    # 1. Process Text Data from request.form
    brand_name = request.form.get('brand_name')
    product_class = request.form.get('product_class')
    abv = request.form.get('abv')
    volume = request.form.get('volume')
    volume_unit = request.form.get('volume_unit')

    # 2. Process the Uploaded File from request.files
    if 'label_image' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['label_image']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        # Secure the filename before saving to prevent attacks
        label_filename = secure_filename(file.filename)
        label_file = os.path.join(app.config['UPLOAD_FOLDER'], label_filename)
        file.save(label_file)

        print("\nINFO: Received Product Details")
        print(f"Brand Name: {brand_name}")
        print(f"Product Class/Type: {product_class}")
        print(f"Alcohol Content: {abv}% ABV")
        print(f"Net Contents: {volume} {volume_unit}")
        print(f"Uploaded File: {label_filename}")
        print("--------------------------------\n")

        result = ocr_process_label(label_file, brand_name, product_class, volume_unit)

        match_level = 0
        brand_match = "No Match"
        brand_ocr = "NA"
        product_class_match = "No Match"
        product_class_ocr = "NA"
        abv_match = "No Match"
        abv_ocr = "NA"
        volume_match = "No Match"
        volume_ocr = "NA"
        volume_unit_match = "No Match"
        volume_unit_ocr = "NA"

        if result['brand']:
            match_level += 1
            brand_match = "Match"
            brand_ocr = result['brand']

        if result['product_class']:
            match_level += 1
            product_class_match = "Match"
            product_class_ocr = result['product_class']

        if result['abv']:
            abv_ocr = result['abv']
            if abv_ocr == abv:
                match_level += 1
                abv_match = "Match"
            

        if result['volume']:
            volume_ocr = result['volume']
            if volume_ocr == volume:
                match_level += 1
                volume_match = "Match"
            

        if result['volume_unit']:
            volume_unit_ocr = result['volume_unit']
            if volume_unit_ocr.lower() == volume_unit.lower():
                match_level += 1
                volume_unit_match = "Match"
            

        match_level = (
                "Full Match" if match_level == 5 
                else "Partial Match" if match_level > 0 
                else "No Match" )

        response_object = jsonify({
            "match_level": match_level,
            "report": [
                {
                    "name": "Brand Name",
                    "input": brand_name,
                    "ocr": brand_ocr,
                    "match": brand_match
                },
                {
                    "name": "Product Class",
                    "input": product_class,
                    "ocr": product_class_ocr,
                    "match": product_class_match
                },
                {
                    "name": "Alcohol Content (ABV)",
                    "input": abv,
                    "ocr": abv_ocr,
                    "match": abv_match
                },
                {
                    "name": "Volume",
                    "input": volume,
                    "ocr": volume_ocr,
                    "match": volume_match
                },
                {
                    "name": "Volume Unit",
                    "input": volume_unit,
                    "ocr": volume_unit_ocr,
                    "match": volume_unit_match
                }
            ]
        })

        print(f"INFO: json={response_object.get_data(as_text=True)}")
        
        return response_object, 200

if __name__ == '__main__':
    app.run()