from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from model.photo_entry import PhotoEntry


class ImageViewerWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.image_label = QLabel("Görsel Seçilmedi")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid #ccc;")
        self.image_label.setMinimumSize(400, 300)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.setLayout(layout)

    def display_photo(self, entry: PhotoEntry):
        pixmap = QPixmap(entry.path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(600, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
        else:
            self.image_label.setText("Görsel yüklenemedi")

    def clear(self):
        self.image_label.clear()
        self.image_label.setText("Görsel Seçilmedi")