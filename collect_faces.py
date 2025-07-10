import cv2
import os
import sys


def collect_faces(label: str, save_dir: str = "data", num_samples: int = 20):
    os.makedirs(save_dir, exist_ok=True)
    person_dir = os.path.join(save_dir, label)
    os.makedirs(person_dir, exist_ok=True)

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Error: Cannot open camera")
        return

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    count = 0
    while count < num_samples:
        ret, frame = cam.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in faces:
            count += 1
            face_img = gray[y:y+h, x:x+w]
            file_path = os.path.join(person_dir, f"{count}.png")
            cv2.imwrite(file_path, face_img)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.imshow('Collecting Faces', frame)
            cv2.waitKey(100)
            if count >= num_samples:
                break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python collect_faces.py <label> [num_samples]")
        sys.exit(1)
    label = sys.argv[1]
    num_samples = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    collect_faces(label, num_samples=num_samples)
