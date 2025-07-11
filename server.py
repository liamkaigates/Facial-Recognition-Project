from flask import Flask, request, jsonify
import os
import cv2
import numpy as np

from train_model import train

app = Flask(__name__)


def save_uploaded_image(file, dir_path):
    os.makedirs(dir_path, exist_ok=True)
    index = len(os.listdir(dir_path)) + 1
    file_path = os.path.join(dir_path, f"{index}.png")
    file.save(file_path)
    return file_path


@app.route('/collect/<label>', methods=['POST'])
def collect(label):
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    file = request.files['image']
    save_dir = os.path.join('data', label)
    path = save_uploaded_image(file, save_dir)
    return jsonify({'saved': path})


@app.route('/train', methods=['POST'])
def train_route():
    train()
    return jsonify({'status': 'trained'})


@app.route('/recognize', methods=['POST'])
def recognize_route():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    file = request.files['image']
    model_path = request.form.get('model', 'trained_model.yml')
    labels_path = request.form.get('labels', 'labels.npy')

    img_array = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(model_path)
    label_map = np.load(labels_path, allow_pickle=True).item()
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=5)

    results = []
    for (x, y, w, h) in faces:
        face_img = img[y:y+h, x:x+w]
        label_id, confidence = recognizer.predict(face_img)
        name = label_map.get(label_id, 'Unknown')
        results.append({'name': name, 'confidence': float(confidence)})

    return jsonify({'results': results})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
