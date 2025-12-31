import sys

from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QWidget,
    QFileDialog,
)
import qdarktheme

from src.widgets.sidebar import Sidebar
from src.widgets.canvas import Canvas


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Annotation Program")
        self.setGeometry(100, 100, 1200, 800)

        layout = QHBoxLayout()

        self.sidebar = Sidebar()
        self.sidebar.open_image_clicked.connect(self.open_image)
        layout.addWidget(self.sidebar, 1)

        self.canvas = Canvas()
        layout.addWidget(self.canvas, 4)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.canvas.load_image(file_path)


app = QApplication(sys.argv)
qdarktheme.setup_theme("auto")

window = MainWindow()
window.show()


if __name__ == "__main__":
    _ = app.exec()
