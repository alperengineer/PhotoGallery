import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow() # ui klasörünün içindeki ana dizaynı burada pencere olarak çalıştırdık
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()