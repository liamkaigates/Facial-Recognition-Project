import SwiftUI

struct ContentView: View {
    @State private var showCollectCamera = false
    @State private var showRecognizeCamera = false
    @State private var label: String = ""
    @State private var recognitionResult: String = ""

    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                TextField("Person Label", text: $label)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding()

                Button("Collect Face") {
                    showCollectCamera = true
                }
                .padding()

                Button("Train Model") {
                    RecognizerAPI.shared.train()
                }
                .padding()

                Button("Recognize Face") {
                    showRecognizeCamera = true
                }
                .padding()

                Text(recognitionResult)
                    .padding()
            }
            .navigationTitle("Face Recognition")
            .sheet(isPresented: $showCollectCamera) {
                CameraView { image in
                    RecognizerAPI.shared.collect(label: label, image: image)
                }
            }
            .sheet(isPresented: $showRecognizeCamera) {
                CameraView { image in
                    RecognizerAPI.shared.recognize(image: image) { result in
                        recognitionResult = result
                    }
                }
            }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
