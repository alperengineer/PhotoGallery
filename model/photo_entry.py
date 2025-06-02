from PyQt5.QtCore import QDate

class PhotoEntry:
    def __init__(self, path, title="", date=None):
        self.path = path
        self.title = title
        self.date = date or QDate.currentDate()

    def to_dict(self):
        return {
            "title": self.title,
            "date": self.date.toString("yyyy-MM-dd")
        }

    @staticmethod
    def from_dict(path, data):
        title = data.get("title", "")
        date_str = data.get("date", "")
        date = QDate.fromString(date_str, "yyyy-MM-dd") if date_str else QDate.currentDate()
        return PhotoEntry(path, title, date)
