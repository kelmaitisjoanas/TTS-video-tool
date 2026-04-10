import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QTimer, Qt
from PyQt5.QtGui import QFont, QPixmap, QDragEnterEvent, QDropEvent

class AudioPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TTS Audio Player with Subtitles")
        self.setGeometry(100, 100, 800, 600)
        self.setAcceptDrops(True)

        self.layout = QVBoxLayout()

        # Image display
        self.image_label = QLabel("Drop images here")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 2px dashed gray; min-height: 300px;")
        self.layout.addWidget(self.image_label)

        # List of audio files
        self.audio_list = QListWidget()
        self.layout.addWidget(self.audio_list)

        # Controls
        controls = QHBoxLayout()
        self.play_btn = QPushButton("Play")
        self.pause_btn = QPushButton("Pause")
        self.next_btn = QPushButton("Next")
        self.export_btn = QPushButton("Export Video")
        controls.addWidget(self.play_btn)
        controls.addWidget(self.pause_btn)
        controls.addWidget(self.next_btn)
        controls.addWidget(self.export_btn)
        self.layout.addLayout(controls)

        # Subtitle label
        self.subtitle_label = QLabel("")
        self.subtitle_label.setFont(QFont("Arial", 20))
        self.subtitle_label.setStyleSheet("color: white; background: black; padding: 10px;")
        self.layout.addWidget(self.subtitle_label)

        self.setLayout(self.layout)

        # Media player
        self.player = QMediaPlayer()
        self.player.positionChanged.connect(self.update_display)

        # Data
        self.audios = []
        self.current_index = -1
        self.current_timings = []
        self.visuals = []  # list of {"path": str, "start": float}

        self.load_audios()

        # Connect buttons
        self.play_btn.clicked.connect(self.play_audio)
        self.pause_btn.clicked.connect(self.pause_audio)
        self.next_btn.clicked.connect(self.next_audio)
        self.export_btn.clicked.connect(self.export_video)
        self.audio_list.itemDoubleClicked.connect(self.select_audio)

    def load_audios(self):
        outputs_dir = "outputs"
        if not os.path.exists(outputs_dir):
            return
        for file in os.listdir(outputs_dir):
            if file.endswith(".json"):
                with open(os.path.join(outputs_dir, file)) as f:
                    data = json.load(f)
                    self.audios.append(data)
                    self.audio_list.addItem(f"{data['voice']}: {data['text'][:50]}...")

    def select_audio(self, item):
        index = self.audio_list.row(item)
        self.load_audio(index)

    def load_audio(self, index):
        if index < 0 or index >= len(self.audios):
            return
        self.current_index = index
        data = self.audios[index]
        audio_path = os.path.join("outputs", data["filename"])
        if os.path.exists(audio_path):
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(audio_path)))
            self.current_timings = data.get("word_timings", [])
            self.subtitle_label.setText("")
            self.visuals = []  # reset visuals for new audio

    def play_audio(self):
        if self.current_index >= 0:
            self.player.play()

    def pause_audio(self):
        self.player.pause()

    def next_audio(self):
        self.load_audio(self.current_index + 1)

    def update_display(self, position):
        # position in ms
        pos_sec = position / 1000.0
        # Update subtitle
        for timing in self.current_timings:
            if timing["start"] <= pos_sec < timing["end"]:
                self.subtitle_label.setText(timing["word"])
                break
        else:
            self.subtitle_label.setText("")
        # Update visual
        for visual in self.visuals:
            if visual["start"] <= pos_sec:
                pixmap = QPixmap(visual["path"])
                if not pixmap.isNull():
                    self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))
                break

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        pos_sec = self.player.position() / 1000.0
        for url in urls:
            path = url.toLocalFile()
            if path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                self.visuals.append({"path": path, "start": pos_sec})
                print(f"Added visual at {pos_sec}s: {path}")

    def export_video(self):
        # Placeholder for export
        print("Exporting video...")
        # Use MoviePy to create video
        from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, TextClip, CompositeVideoClip
        if self.current_index < 0:
            return
        data = self.audios[self.current_index]
        audio_path = os.path.join("outputs", data["filename"])
        if not os.path.exists(audio_path):
            return
        audio = AudioFileClip(audio_path)
        clips = [audio]
        prev_end = 0
        for i, visual in enumerate(self.visuals):
            start = visual["start"]
            duration = audio.duration - start if i == len(self.visuals) - 1 else self.visuals[i+1]["start"] - start
            img_clip = ImageClip(visual["path"], duration=duration).set_start(start)
            # Add fade in/out
            img_clip = img_clip.fadein(0.5).fadeout(0.5)
            clips.append(img_clip)
        # Add subtitles
        for timing in self.current_timings:
            txt_clip = TextClip(timing["word"], fontsize=50, color='white', bg_color='black').set_position('bottom').set_duration(timing["end"] - timing["start"]).set_start(timing["start"])
            clips.append(txt_clip)
        video = CompositeVideoClip(clips)
        video.write_videofile("output_video.mp4", fps=24)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = AudioPlayer()
    player.show()
    sys.exit(app.exec_())
