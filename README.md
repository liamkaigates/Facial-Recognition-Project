# Facial Recognition Project

This project demonstrates a simple facial recognition pipeline using **Python** and **OpenCV**. The workflow consists of three steps:

1. **Collect Faces** – capture face images from the webcam and store them in the `data/` directory.
2. **Train Model** – train an LBPH (Local Binary Pattern Histogram) recognizer based on the collected images.
3. **Recognize Faces** – run real‑time recognition using the trained model.

## Setup

Install the dependencies with:

```bash
pip install -r requirements.txt
```

## Collecting Faces

Run the following command and replace `PERSON_NAME` with a label for the captured faces:

```bash
python collect_faces.py PERSON_NAME 20
```

This command captures 20 face images from the webcam and stores them in `data/PERSON_NAME/`.

## Training

After collecting images for one or more people, train the model:

```bash
python train_model.py
```

The trained model is saved to `trained_model.yml`, and a label map is stored in `labels.npy`.

## Recognition

To perform real‑time recognition using the webcam:

```bash
python recognize.py
```

Press **`q`** to exit the recognition window.

## Notes

This project uses OpenCV's built‑in Haar cascade for face detection and the LBPH face recognizer for identification. Ensure you have a webcam attached when running the scripts.
