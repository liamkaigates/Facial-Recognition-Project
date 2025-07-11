import SwiftUI

struct ContentView: View {
    @State private var label: String = ""
    @State private var showingCamera = false
    @State private var mode: Mode = .collect
    @State private var results: [RecognitionResult] = []

    enum Mode { case collect, recognize }

    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                TextField("Label", text: $label)
                    .textFieldStyle(.roundedBorder)
                    .padding(.horizontal)

                HStack {
                    Button("Collect Face") {
                        mode = .collect
                        showingCamera = true
                    }
                    .buttonStyle(.bordered)

                    Button("Recognize") {
                        mode = .recognize
                        showingCamera = true
                    }
                    .buttonStyle(.bordered)
                }

                Button("Train Model") {
                    Task { try? await RecognizerAPI.train() }
                }
                .buttonStyle(.borderedProminent)

                if !results.isEmpty {
                    List(results, id: \.name) { item in
                        VStack(alignment: .leading) {
                            Text(item.name)
                            Text(String(format: "%.2f", item.confidence))
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                    }
                }
            }
            .navigationTitle("Face Rec")
        }
        .sheet(isPresented: $showingCamera) {
            CameraView { image in
                Task {
                    if mode == .collect {
                        try? await RecognizerAPI.collect(label: label, image: image)
                    } else {
                        results = (try? await RecognizerAPI.recognize(image: image)) ?? []
                    }
                }
            }
        }
    }
}

#Preview {
    ContentView()
}
