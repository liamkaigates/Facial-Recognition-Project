import cv2
import numpy as np
import sys


def recognize(model_path: str = 'trained_model.yml', labels_path: str = 'labels.npy'):
    if not hasattr(cv2, 'face'):
        print("Error: OpenCV is missing the 'face' module. Install opencv-contrib-python.")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(model_path)
    label_map = np.load(labels_path, allow_pickle=True).item()

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print('Error: Cannot open camera')
        return

    while True:
        ret, frame = cam.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in faces:
            face_img = gray[y:y+h, x:x+w]
            label_id, confidence = recognizer.predict(face_img)
            name = label_map.get(label_id, 'Unknown')
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"{name} {confidence:.2f}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow('Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    model_path = sys.argv[1] if len(sys.argv) > 1 else 'trained_model.yml'
    labels_path = sys.argv[2] if len(sys.argv) > 2 else 'labels.npy'
    recognize(model_path, labels_path)
