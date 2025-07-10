import os
import cv2
import numpy as np


def prepare_training_data(data_dir: str = 'data'):
    faces = []
    labels = []
    label_map = {}
    label_id = 0

    if not os.path.isdir(data_dir):
        return faces, np.array(labels), label_map

    for person_name in os.listdir(data_dir):
        person_path = os.path.join(data_dir, person_name)
        if not os.path.isdir(person_path):
            continue
        label_map[label_id] = person_name
        for img_name in os.listdir(person_path):
            img_path = os.path.join(person_path, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            faces.append(img)
            labels.append(label_id)
        label_id += 1
    return faces, np.array(labels), label_map


def train(data_dir: str = 'data', model_path: str = 'trained_model.yml', labels_path: str = 'labels.npy'):
    faces, labels, label_map = prepare_training_data(data_dir)
    if not faces:
        print('No training data found.')
        return
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, labels)
    recognizer.save(model_path)
    np.save(labels_path, label_map)
    print('Training completed.')


if __name__ == '__main__':
    train()
