import Foundation
import UIKit

struct RecognitionResult: Codable {
    let name: String
    let confidence: Double
}

enum RecognizerAPI {
    static let baseURL = URL(string: "http://localhost:8000")!

    static func collect(label: String, image: UIImage) async throws {
        let url = baseURL.appendingPathComponent("collect").appendingPathComponent(label)
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        request.httpBody = try formData(boundary: boundary, image: image)
        _ = try await URLSession.shared.data(for: request)
    }

    static func train() async throws {
        let url = baseURL.appendingPathComponent("train")
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        _ = try await URLSession.shared.data(for: request)
    }

    static func recognize(image: UIImage) async throws -> [RecognitionResult] {
        let url = baseURL.appendingPathComponent("recognize")
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        request.httpBody = try formData(boundary: boundary, image: image)
        let (data, _) = try await URLSession.shared.data(for: request)
        let decoded = try JSONDecoder().decode(Response.self, from: data)
        return decoded.results
    }

    private static func formData(boundary: String, image: UIImage) throws -> Data {
        var data = Data()
        guard let imgData = image.jpegData(compressionQuality: 0.8) else { return data }
        let lineBreak = "\r\n"
        data.append("--\(boundary)\r\n".data(using: .utf8)!)
        data.append("Content-Disposition: form-data; name=\"image\"; filename=\"image.jpg\"\r\n".data(using: .utf8)!)
        data.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
        data.append(imgData)
        data.append(lineBreak.data(using: .utf8)!)
        data.append("--\(boundary)--\r\n".data(using: .utf8)!)
        return data
    }

    private struct Response: Codable {
        let results: [RecognitionResult]
    }
}
