from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal


class ImageThumbnailWidget(QWidget):
    clicked = pyqtSignal()

    def __init__(self, image_path, thumbnail_size=(120, 90), parent=None):
        super().__init__(parent)
        self.image_path = image_path

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        pixmap = QPixmap(image_path).scaled(
            *thumbnail_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.image_label.setPixmap(pixmap)

        self.name_label = QLabel(image_path.split("/")[-1])
        self.name_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.name_label)

        self.setLayout(layout)
        self.setFixedSize(thumbnail_size[0] + 20, thumbnail_size[1] + 40)
        self.setStyleSheet("""
            QWidget {
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
            QWidget:hover {
                background-color: #e6f7ff;
            }
        """)

    # mousePressEvent ile sol tıklama yapıldığında, clicked sinyali yayılır (emit() fonskiyonu sayesinde
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()