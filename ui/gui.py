import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QSize

class RoadmapMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Roadmap")
        self.setMinimumSize(QSize(600, 400))

def run_application():
    app = QApplication(sys.argv)
    window = RoadmapMainWindow()
    window.show()
    sys.exit(app.exec())