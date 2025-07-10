# iOS Interface

This folder contains a simple SwiftUI application that communicates with a local
Python server to perform face collection, training and recognition.

## Setup

1. Run the Python server:

   ```bash
   python server.py
   ```

   The server listens on `http://localhost:8000`.

2. Open the Swift files in Xcode and build the app. The project uses three
   simple views (`FaceRecApp.swift`, `ContentView.swift` and `CameraView.swift`)
   and a helper `RecognizerAPI` class for network requests.

3. The app lets you:

   - Capture faces for a given label.
   - Trigger training of the model.
   - Capture a face for recognition.

Make sure the device running the app can reach the server URL.
