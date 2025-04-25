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

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --------- Download Models from Hugging Face if Not Present ---------
def download_from_hf(url, dest_path):
    print(f"Downloading {url} ...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(dest_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    # Print first 200 bytes for debug
    with open(dest_path, "rb") as f:
        head = f.read(200)
        print(f"First 200 bytes of {os.path.basename(dest_path)}: {head}")
    # Print file size
    print(f"Downloaded file size: {os.path.getsize(dest_path)} bytes")

for filename, url in MODEL_FILES.items():
    local_path = os.path.join(UPLOAD_DIR, filename)
    # Download if missing or if file is suspiciously small (<1MB)
    if not os.path.exists(local_path) or os.path.getsize(local_path) < 1_000_000:
        download_from_hf(url, local_path)
    else:
        print(f"{filename} already exists, skipping download.")

# --------- Load YOLO Models ---------
models = []
for filename in MODEL_FILES:
    model_path = os.path.join(UPLOAD_DIR, filename)
    try:
        models.append(YOLO(model_path))
        print(f"Loaded model: {filename}")
    except Exception as e:
        print(f"Failed to load model {filename}: {e}")

# --------- Nutrition Data ---------
calorie_data = {
    'apple': 52, 'avocado': 160, 'banana': 89, 'bean': 347,
    'bitter_gourd': 17, 'bottle_gourd': 14, 'brinjal': 25,
    'broccoli': 34, 'cabbage': 25, 'capsicum': 31, 'carrot': 41,
    'cauliflower': 25, 'cherry': 50, 'cucumber': 15, 'kiwi': 61,
    'mango': 60, 'orange': 47, 'papaya': 43, 'pineapple': 50,
    'potato': 77, 'pumpkin': 26, 'radish': 16, 'strawberry': 32,
    'tomato': 18, 'watermelon': 30
}

nutrition_info = {
    'apple': {
        'advantages': 'Rich in fiber, vitamin C, and antioxidants.',
        'disadvantages': 'May cause bloating or digestive discomfort if overeaten.',
        'benefits': 'Supports heart health, aids weight management, and boosts immunity.'
    },
    'avocado': {
        'advantages': 'High in healthy fats, potassium, and fiber.',
        'disadvantages': 'Calorie-dense; excessive intake may contribute to weight gain.',
        'benefits': 'Supports heart health, improves cholesterol, and aids nutrient absorption.'
    },
    'banana': {
        'advantages': 'Good source of potassium, vitamin B6, and fiber.',
        'disadvantages': 'High sugar content; may affect blood sugar in diabetics.',
        'benefits': 'Supports energy levels, digestion, and heart health.'
    },
    'bean': {
        'advantages': 'High in protein, fiber, and essential minerals.',
        'disadvantages': 'May cause gas or bloating in some individuals.',
        'benefits': 'Supports muscle growth, digestive health, and blood sugar control.'
    },
    'bitter_gourd': {
        'advantages': 'Low in calories, rich in vitamin C and antioxidants.',
        'disadvantages': 'Bitter taste; may cause stomach discomfort in excess.',
        'benefits': 'Helps regulate blood sugar and supports immune function.'
    },
    'bottle_gourd': {
        'advantages': 'Low in calories, hydrating, rich in vitamin C.',
        'disadvantages': 'May cause digestive upset if consumed raw in large amounts.',
        'benefits': 'Aids hydration, supports digestion, and helps in weight loss.'
    },
    'brinjal': {
        'advantages': 'Rich in fiber, antioxidants, and vitamins.',
        'disadvantages': 'May cause allergies in sensitive individuals.',
        'benefits': 'Supports heart health and provides anti-inflammatory benefits.'
    },
    'broccoli': {
        'advantages': 'High in vitamins C, K, and fiber; contains sulforaphane.',
        'disadvantages': 'May cause gas or bloating.',
        'benefits': 'Boosts immunity, supports bone health, and may reduce cancer risk.'
    },
    'cabbage': {
        'advantages': 'Rich in vitamin K, C, and fiber.',
        'disadvantages': 'Can cause flatulence if eaten in excess.',
        'benefits': 'Supports digestion and may lower cholesterol.'
    },
    'capsicum': {
        'advantages': 'High in vitamin C, A, and antioxidants.',
        'disadvantages': 'Rarely, may cause allergic reactions.',
        'benefits': 'Supports eye health and boosts immunity.'
    },
    'carrot': {
        'advantages': 'Excellent source of beta-carotene, fiber, and vitamin K.',
        'disadvantages': 'Excessive intake may cause carotenemia (orange skin).',
        'benefits': 'Promotes eye health and supports immune function.'
    },
    'cauliflower': {
        'advantages': 'High in vitamin C, K, and fiber; low in calories.',
        'disadvantages': 'May cause gas or bloating.',
        'benefits': 'Supports digestion and provides antioxidants.'
    },
    'cherry': {
        'advantages': 'Rich in antioxidants, vitamin C, and fiber.',
        'disadvantages': 'High sugar content; overconsumption may affect blood sugar.',
        'benefits': 'Reduces inflammation and supports heart health.'
    },
    'cucumber': {
        'advantages': 'Hydrating, low in calories, contains vitamin K.',
        'disadvantages': 'Low in protein and fat; may not be filling.',
        'benefits': 'Aids hydration and supports skin health.'
    },
    'kiwi': {
        'advantages': 'High in vitamin C, K, and fiber.',
        'disadvantages': 'May cause allergies in sensitive individuals.',
        'benefits': 'Boosts immunity and aids digestion.'
    },
    'mango': {
        'advantages': 'Rich in vitamin A, C, and antioxidants.',
        'disadvantages': 'High sugar content; excessive intake may affect blood sugar.',
        'benefits': 'Supports eye health and boosts immunity.'
    },
    'orange': {
        'advantages': 'Excellent source of vitamin C and fiber.',
        'disadvantages': 'Acidic; may cause heartburn in some people.',
        'benefits': 'Boosts immunity and supports skin health.'
    },
    'papaya': {
        'advantages': 'High in vitamin C, A, and digestive enzymes.',
        'disadvantages': 'May cause allergic reactions in some people.',
        'benefits': 'Aids digestion and supports immune health.'
    },
    'pineapple': {
        'advantages': 'Rich in vitamin C, manganese, and bromelain enzyme.',
        'disadvantages': 'Acidic; may cause mouth irritation.',
        'benefits': 'Aids digestion and supports immune function.'
    },
    'potato': {
        'advantages': 'Good source of vitamin C, B6, and potassium.',
        'disadvantages': 'High glycemic index; may spike blood sugar.',
        'benefits': 'Supports energy and heart health.'
    },
    'pumpkin': {
        'advantages': 'High in vitamin A, fiber, and antioxidants.',
        'disadvantages': 'Low protein content.',
        'benefits': 'Supports eye health and boosts immunity.'
    },
    'radish': {
        'advantages': 'Low in calories, rich in vitamin C and fiber.',
        'disadvantages': 'May cause gas if eaten in excess.',
        'benefits': 'Supports digestion and detoxification.'
    },
    'strawberry': {
        'advantages': 'Rich in vitamin C, manganese, and antioxidants.',
        'disadvantages': 'May cause allergies in some individuals.',
        'benefits': 'Promotes heart health and boosts immunity.'
    },
    'tomato': {
        'advantages': 'High in vitamin C, potassium, and lycopene.',
        'disadvantages': 'Acidic; may cause heartburn.',
        'benefits': 'Supports heart health and provides antioxidants.'
    },
    'watermelon': {
        'advantages': 'Hydrating, rich in vitamin C, A, and antioxidants.',
        'disadvantages': 'High glycemic index; may affect blood sugar.',
        'benefits': 'Aids hydration and supports heart health.'
    }
}

# --------- Flask App Setup ---------
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

@app.route('/contact.html')
def contact_html():
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
        # Collect detections from all models
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