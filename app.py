from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from ultralytics import YOLO

# --------- Constants ---------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --------- Model Files (Pre-downloaded) ---------
MODEL_FILES = [
    "yolo11x.pt",
    "yolov10l.pt",
    "yolov8x-oiv7.pt",
    "yolov9e.pt"
]

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
# Add your `calorie_data` and `nutrition_info` dictionaries here
calorie_data = {
    "banana": 89,
    "apple": 52,
    "orange": 47
    # Add more as needed
}

nutrition_info = {
    "banana": {
        "advantages": "Rich in potassium.",
        "disadvantages": "High in sugar for diabetics.",
        "benefits": "Supports heart health."
    },
    "apple": {
        "advantages": "High in fiber.",
        "disadvantages": "May cause bloating in excess.",
        "benefits": "Helps in weight loss."
    },
    "orange": {
        "advantages": "Vitamin C rich.",
        "disadvantages": "Can be acidic.",
        "benefits": "Boosts immunity."
    }
}

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
