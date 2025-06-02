import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QListWidget, QLabel, QVBoxLayout,
    QHBoxLayout, QPushButton, QLineEdit, QDateEdit, QFileDialog,
    QMessageBox, QSplitter, QListWidgetItem, QListView
)
from PyQt5.QtCore import Qt, QDate, QSize
from PyQt5.QtGui import QPixmap, QIcon
from service.file_manager import load_data, save_data
from model.photo_entry import PhotoEntry
from widgets.image_viewer_widget import ImageViewerWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # main_window.py'nin dizini
        icon_path = os.path.join(BASE_DIR, "ic_logo.ico")
        self.setWindowIcon(QIcon(icon_path))

        self.photo_data: dict[str, PhotoEntry] = {}
        self.image_viewer = ImageViewerWidget()


        self.setWindowTitle("Seyahat Fotoğraf Günlüğü")
        self.resize(1000, 600)

        self.photo_paths = []
        self.current_index = -1
        self.photo_data = {}

        saved_data = load_data()
        for path, entry_data in saved_data.items():
            self.photo_data[path] = PhotoEntry.from_dict(path,entry_data)

        self.setup_ui()

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Sol: Thumbnail listesi
        self.photo_list = QListWidget()
        self.photo_list.itemClicked.connect(self.on_photo_selected)

        # Sağ: Görsel ve form alanları
        self.photo_label = QLabel("Seçilen görsel...")
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setMinimumSize(400, 300)

        self.title_edit = QLineEdit()
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())

        self.photo_list.setViewMode(QListView.IconMode)
        self.photo_list.setIconSize(QSize(100, 100))
        self.photo_list.setResizeMode(QListWidget.Adjust)
        self.photo_list.setSpacing(10)

        # clicked() sinyali, save_entry() slot'una bağlanarak tıklama olayında metodun tetiklenmesi sağlanır
        save_button = QPushButton("Kaydet")
        save_button.clicked.connect(self.save_entry)

        # clicked() sinyali, next_button() slot'una bağlanarak tıklama olayında metodun tetiklenmesi sağlanır
        next_button = QPushButton("İleri")
        next_button.clicked.connect(self.next_image)

        # clicked() sinyali, prev_button() slot'una bağlanarak tıklama olayında metodun tetiklenmesi sağlanır
        prev_button = QPushButton("Geri")
        prev_button.clicked.connect(self.prev_image)

        # clicked() sinyali, open_folder_button() slot'una bağlanarak tıklama olayında metodun tetiklenmesi sağlar
        open_folder_button = QPushButton("Klasör Aç")
        open_folder_button.clicked.connect(self.select_folder)

        # Sağ tarafın layout tasarımı
        right_layout = QVBoxLayout()
        right_layout.addWidget(open_folder_button)
        right_layout.addWidget(self.image_viewer, stretch=2)
        right_layout.addWidget(QLabel("Başlık:"))
        right_layout.addWidget(self.title_edit)
        right_layout.addWidget(QLabel("Tarih:"))
        right_layout.addWidget(self.date_edit)
        right_layout.addWidget(save_button)
        right_layout.addWidget(prev_button)
        right_layout.addWidget(next_button)

        splitter = QSplitter()
        splitter.addWidget(self.photo_list)

        right_panel = QWidget()
        right_panel.setLayout(right_layout)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(1, 3)

        layout = QHBoxLayout()
        layout.addWidget(splitter)
        main_widget.setLayout(layout)

    # Klasör seçimi
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Klasör Seç")
        if not folder:
            QMessageBox.warning(self, "Uyarı", "Klasör seçilmedi.")
            return
        self.load_photos(folder)

    # Klasör içinde eğere .png, .jpg ve .jpeg uzantılı dosyaları yükleme işlemi
    def load_photos(self, folder):
        self.photo_paths = []
        self.photo_list.clear()
        self.current_index = -1

        for file in os.listdir(folder):
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                full_path = os.path.join(folder, file)
                self.photo_paths.append(full_path)

                pixmap = QPixmap(full_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                item = QListWidgetItem(QIcon(pixmap), file)
                self.photo_list.addItem(item)

        if not self.photo_paths:
            QMessageBox.information(self, "Bilgi", "Klasörde geçerli görsel bulunamadı.")
        else:
            self.current_index = 0
            self.photo_list.setCurrentRow(0)
            self.display_image()

    # Sol panelde seçilen dosyanın index ve satır değeri alınır
    def on_photo_selected(self, item):
        index = self.photo_list.row(item)
        self.current_index = index
        self.display_image()

    # Seçilen dosyayı sağ panelde görüntüleme
    def display_image(self):
        path = self.photo_paths[self.current_index]
        entry = self.photo_data.get(path)

        if not entry:
            entry = PhotoEntry(path)
            self.photo_data[path] = entry

        self.image_viewer.display_photo(entry)
        self.title_edit.setText(entry.title)
        self.date_edit.setDate(entry.date)

    # Seçilen dosyayı Başlık(title) boş geçilmez ise .json uzantılı olarak kaydeder. Eğer başlık boş bırakılarak kaydedilmez ise kullanıcaya uyarı mesajı verilir
    def save_entry(self):
        if self.current_index == -1:
            QMessageBox.warning(self, "Uyarı", "Herhangi bir görsel seçilmedi.")
            return

        path = self.photo_paths[self.current_index]
        title = self.title_edit.text()
        date = self.date_edit.date()

        if not title.strip():
            QMessageBox.warning(self, "Uyarı", "Başlık boş bırakılamaz.")
            return

        entry = PhotoEntry(path, title, date)
        self.photo_data[path] = entry

        json_data = {p: e.to_dict() for p, e in self.photo_data.items()}
        save_data(json_data)

        QMessageBox.information(self, "Başarılı", "Girdi kaydedildi.")

    # Açılan klasörde index'e bağlı olarak fotoğrafları index numarası artacak şekilde ilerletir
    def next_image(self):
        if self.current_index < len(self.photo_paths) - 1:
            self.current_index += 1
            self.photo_list.setCurrentRow(self.current_index)
            self.display_image()

    # Açılan klasörde index'e bağlı olarak fotoğrafları index numarası azalacak şekilde ilerletir
    def prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.photo_list.setCurrentRow(self.current_index)
            self.display_image()