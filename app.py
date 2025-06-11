from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import gdown
from ultralytics import YOLO

# --------- Constants ---------
UPLOAD_DIR = "models"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --------- Google Drive File IDs for Models ---------
MODEL_FILES = {
    "yolo11x.pt": "1dvKoq8wMc_xqXtDHQX7rnc0n4PTsQOa0",
    "yolov10l.pt": "1XCN68J8d2C_DbB2F8ak6AOOF7wyfaufO",
    "yolov8x-oiv7.pt": "1Hz8IVZ8YR47Ly0smoOHkmvnf6g1bB4ee",
    "yolov9e.pt": "156UHX51YScgFby-m5r1yWH6TqRf-AH6B"
}

# --------- Function to download from Google Drive ---------
def download_from_drive(file_id, dest_path):
    url = f"https://drive.google.com/uc?id={file_id}"
    print(f"Downloading from: {url}")
    gdown.download(url, dest_path, quiet=False)

# --------- Download Models if Needed ---------
for filename, file_id in MODEL_FILES.items():
    model_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(model_path) or os.path.getsize(model_path) < 1_000_000:
        print(f"{filename} not found or too small, downloading...")
        download_from_drive(file_id, model_path)
    else:
        print(f"{filename} already exists, skipping download.")

# --------- Load YOLO Models ---------
models = []
for filename in MODEL_FILES:
    model_path = os.path.join(UPLOAD_DIR, filename)
    try:
        print(f"Loading model: {filename}")
        models.append(YOLO(model_path))
    except Exception as e:
        print(f"Failed to load model {filename}: {e}")

# --------- Nutrition Data ---------
# (same calorie_data and nutrition_info dictionaries as your code)

# --------- Flask Setup ---------
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/images')
def images():
    return render_template('images.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    image_path = os.path.join(UPLOAD_DIR, image_file.filename)
    image_file.save(image_path)

    try:
        union_detections = {}
        for model in models:
            results = model(image_path)
            names = results[0].names
            for box in results[0].boxes:
                class_id = int(box.cls[0])
                label = names[class_id]
                norm_label = label.strip().lower().replace(" ", "_")
                conf = float(box.conf[0])
                if norm_label in calorie_data:
                    if norm_label not in union_detections:
                        union_detections[norm_label] = {
                            'label': label,
                            'confidences': [conf],
                            'count': 1
                        }
                    else:
                        union_detections[norm_label]['confidences'].append(conf)
                        union_detections[norm_label]['count'] += 1

        detected_items = []
        for norm_label, info in union_detections.items():
            cal = calorie_data[norm_label]
            nutri = nutrition_info.get(norm_label, {})
            avg_conf = sum(info['confidences']) / len(info['confidences'])
            detected_items.append({
                'name': info['label'],
                'quantity': info['count'],
                'confidence': f"{avg_conf*100:.1f}%",
                'calorific_value': f"{cal} kcal per 100g",
                'advantages': nutri.get('advantages', 'N/A'),
                'disadvantages': nutri.get('disadvantages', 'N/A'),
                'benefits': nutri.get('benefits', 'N/A'),
                'total_calories': f"{cal * info['count']} kcal (estimated total)"
            })

        response = {'detections': detected_items}

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(image_path):
            os.remove(image_path)

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
