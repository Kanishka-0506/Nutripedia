
# 🥦 NutriPedia – Smart Nutrition Prediction from Food Images

**NutriPedia** is a smart web application that predicts the nutritional value of food items using deep learning. Users can upload an image of a food item and receive predictions about its name, calories, benefits, disadvantages, and more.

🔗 **Live Demo**: [Click to Open NutriPedia](https://huggingface.co/spaces/Varsaa/NutriPedia)

---

## 🚀 Features

- 📸 Upload a food image and get predictions in real time
- 🧠 Uses **multiple YOLO models** to improve accuracy
- 🔄 Merges predictions from `yolo11x.pt`, `yolov10l.pt`, `yolov8x-oiv7.pt`, `yolov9e.pt`
- 📊 Displays:
  - Food item name
  - Calorific value
  - Advantages and disadvantages
- 🖥️ Beautiful UI with **dark mode** and **responsive design**
- 🐳 Deployed using Docker on Hugging Face Spaces

---

## 🛠️ Tech Stack

| Layer        | Technologies Used                                 |
|--------------|----------------------------------------------------|
| Frontend     | HTML, CSS, Bootstrap, JavaScript                  |
| Backend      | Flask (Python)                                     |
| ML Models    | YOLOv8 / YOLOv9 / YOLOv10 / YOLOv11 (PyTorch)     |
| Deployment   | Hugging Face Spaces + Docker                      |

---




