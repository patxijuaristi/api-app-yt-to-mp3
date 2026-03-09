class VideoInfo {
  final String title;
  final String author;
  final String duration;
  final String? thumbnail;

  VideoInfo({
    required this.title,
    required this.author,
    required this.duration,
    this.thumbnail,
  });

  factory VideoInfo.fromJson(Map<String, dynamic> json) {
    return VideoInfo(
      title: json['title'] ?? 'Unknown',
      author: json['author'] ?? 'Unknown',
      duration: json['duration'] ?? '0:00',
      thumbnail: json['thumbnail'],
    );
  }
}
