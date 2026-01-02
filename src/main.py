import sys

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
    imagesPaths: list[str] = []
    currImgIdx: int = 0

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MAReK")
        self.setGeometry(100, 100, 1200, 800)

        layout = QHBoxLayout()

        self.canvas = Canvas()
        self.sidebar = Sidebar()

        self.sidebar.open_image_clicked.connect(self.open_image)
        self.sidebar.pen.connect(self.canvas.set_tool_pen)
        self.sidebar.eraser.connect(self.canvas.set_tool_eraser)
        self.sidebar.save.connect(self.canvas.save)
        self.sidebar.nextImage.connect(self.next_image)
        self.sidebar.prevImage.connect(self.prev_image)
        layout.addWidget(self.canvas, 4)

        layout.addWidget(self.sidebar, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def open_image(self):
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Open Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)",
        )
        self.images_paths = file_paths
        self.currImgIdx = 0
        if file_paths:
            self.canvas.load_image(file_paths[self.currImgIdx])

    def next_image(self):
        self.currImgIdx = (self.currImgIdx + 1) % len(self.images_paths)
        self.canvas.load_image(self.images_paths[self.currImgIdx])

    def prev_image(self):
        self.currImgIdx = (self.currImgIdx - 1) % len(self.images_paths)
        self.canvas.load_image(self.images_paths[self.currImgIdx])



app = QApplication(sys.argv)
qdarktheme.setup_theme("auto")

window = MainWindow()
window.show()


if __name__ == "__main__":
    _ = app.exec()
