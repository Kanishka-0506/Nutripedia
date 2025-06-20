from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import requests
from ultralytics import YOLO

# --------- Hugging Face Model Download Links ---------
MODEL_FILES = {
    "yolo11x.pt": "https://huggingface.co/gokusaiyan4096/nutripedia-yolo-models/resolve/main/yolo11x.pt",
    "yolov10l.pt": "https://huggingface.co/gokusaiyan4096/nutripedia-yolo-models/resolve/main/yolov10l.pt",
    "yolov8x-oiv7.pt": "https://huggingface.co/gokusaiyan4096/nutripedia-yolo-models/resolve/main/yolov8x-oiv7.pt",
    "yolov9e.pt": "https://huggingface.co/gokusaiyan4096/nutripedia-yolo-models/resolve/main/yolov9e.pt"
}

UPLOAD_DIR = "/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def download_from_hf(url, dest_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(dest_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

for filename, url in MODEL_FILES.items():
    local_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(local_path) or os.path.getsize(local_path) < 1_000_000:
        download_from_hf(url, local_path)

# --------- Load YOLO Models ---------
models = []
for filename in MODEL_FILES:
    model_path = os.path.join(UPLOAD_DIR, filename)
    try:
        models.append(YOLO(model_path))
    except Exception as e:
        print(f"Failed to load model {filename}: {e}")

# --------- Nutrition and Calorie Data ---------
calorie_data = {
    "apple": 52,
    "banana": 89,
    "carrot": 41,
    "pineapple": 50,
    "strawberry": 33
}

nutrition_info = {
    "apple": {
        "advantages": "Rich in fiber and vitamin C",
        "disadvantages": "May cause digestive issues in excess",
        "benefits": "Good for heart health"
    },
    "banana": {
        "advantages": "Rich in potassium and fiber",
        "disadvantages": "High in sugar",
        "benefits": "Good for energy and digestion"
    },
    "carrot": {
        "advantages": "High in beta-carotene and vitamin A",
        "disadvantages": "Can cause carotenemia in excess",
        "benefits": "Improves eye health"
    },
    "pineapple": {
        "advantages": "Rich in vitamin C and enzymes",
        "disadvantages": "Can irritate mouth due to bromelain",
        "benefits": "Supports immunity and digestion"
    },
    "strawberry": {
        "advantages": "High in antioxidants and vitamin C",
        "disadvantages": "Can cause allergies in some",
        "benefits": "Boosts skin health"
    }
}

# --------- Flask App ---------
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
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
            names = model.names

            for box in results[0].boxes:
                if not hasattr(box, 'cls') or not hasattr(box, 'conf'):
                    continue

                class_id = int(box.cls[0])
                conf = float(box.conf[0])
                label = names.get(class_id, f"cls_{class_id}")
                norm_label = label.strip().lower().replace(" ", "_")

                print(f"Detected: {label} ({norm_label}) with confidence {conf:.2f}")

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
            cal = calorie_data.get(norm_label, None)
            nutri = nutrition_info.get(norm_label, {})
            avg_conf = sum(info['confidences']) / len(info['confidences'])

            item = {
                'name': info['label'],
                'quantity': info['count'],
                'confidence': f"{avg_conf * 100:.1f}%",
                'calorific_value': f"{cal} kcal per 100g" if cal else "Unknown",
                'advantages': nutri.get('advantages', 'N/A'),
                'disadvantages': nutri.get('disadvantages', 'N/A'),
                'benefits': nutri.get('benefits', 'N/A'),
                'total_calories': f"{cal * info['count']} kcal (estimated total)" if cal else "Unknown"
            }

            detected_items.append(item)

        if not detected_items:
            return jsonify({'message': 'No fruits or vegetables detected.'})

        return jsonify({'detections': detected_items})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(image_path):
            os.remove(image_path)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 7860)))
