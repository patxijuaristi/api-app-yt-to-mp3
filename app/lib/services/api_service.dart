import 'dart:convert';
import 'dart:io';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:http/http.dart' as http;
import 'package:path_provider/path_provider.dart';
import '../models/video_model.dart';

class ApiService {
  static String get baseUrl => dotenv.env['API_BASE_URL'] ?? 'http://localhost:8000';

  Future<VideoInfo> getVideoInfo(String url) async {
    final response = await http.post(
      Uri.parse('$baseUrl/info'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'url': url}),
    );

    if (response.statusCode == 200) {
      return VideoInfo.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to get video info: ${response.body}');
    }
  }

  Future<void> downloadMp3(
    String url, {
    Function(double)? onProgress,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/download'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'url': url}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final downloadUrl = '$baseUrl${data['download_url']}';
      
      final downloadResponse = await http.Client().send(
        http.Request('GET', Uri.parse(downloadUrl)),
      );

      final contentLength = downloadResponse.contentLength ?? 0;
      final bytes = <int>[];
      int received = 0;

      await for (final chunk in downloadResponse.stream) {
        bytes.addAll(chunk);
        received += chunk.length;
        if (contentLength > 0 && onProgress != null) {
          onProgress(received / contentLength);
        }
      }

      final directory = await getApplicationDocumentsDirectory();
      final filename = data['filename'] ?? 'audio.mp3';
      final file = File('${directory.path}/$filename');
      await file.writeAsBytes(bytes);
    } else {
      throw Exception('Failed to download: ${response.body}');
    }
  }
}
