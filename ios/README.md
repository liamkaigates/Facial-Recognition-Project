# iOS Interface

This folder contains a simple SwiftUI application that communicates with a local
Python server to perform face collection, training and recognition.

## Setup

1. Run the Python server:

   ```bash
   python server.py
   ```

   The server listens on `http://localhost:8000`.

2. Open the `ios/Facial Recognition` project in **Xcode**.

   The app contains the SwiftUI files `Facial_RecognitionApp.swift`,
   `ContentView.swift`, `CameraView.swift` and the helper `RecognizerAPI`.
   Select a simulator or device and press **Run** (`Cmd+R`) to build and launch
   the app.

3. The app lets you:

   - Capture faces for a given label.
   - Trigger training of the model.
   - Capture a face for recognition.

Make sure the device running the app can reach the server URL.
