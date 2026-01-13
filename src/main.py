from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QWidget,
)

from src.widgets.canvas import Canvas
from src.widgets.sidebar import Sidebar


class MainWindow(QMainWindow):
    imagesPaths: list[str] = []
    currImgIdx: int = 0
    objects_map: dict[str, list] = {}

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MAReK")
        self.setGeometry(100, 100, 1200, 800)

        layout = QHBoxLayout()

        self.canvas = Canvas()
        self.sidebar = Sidebar()

        self.sidebar.open_image_clicked.connect(self.open_images)
        self.sidebar.hand.connect(self.canvas.set_tool_hand)
        self.sidebar.pen.connect(self.canvas.set_tool_pen)
        self.sidebar.eraser.connect(self.canvas.set_tool_eraser)
        self.sidebar.save.connect(self.canvas.save)
        self.sidebar.nextImage.connect(self.next_image)
        self.sidebar.prevImage.connect(self.prev_image)
        self.canvas.objects_updated.connect(self.update_objects_map)

        layout.addWidget(self.canvas, 4)

        layout.addWidget(self.sidebar, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def open_images(self):
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Open Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)",
        )
        self.images_paths = file_paths
        self.currImgIdx = 0
        if file_paths:
            self._load_image_with_objects(file_paths[self.currImgIdx])

    def next_image(self):
        self.currImgIdx = (self.currImgIdx + 1) % len(self.images_paths)
        self._load_image_with_objects(self.images_paths[self.currImgIdx])

    def prev_image(self):
        self.currImgIdx = (self.currImgIdx - 1) % len(self.images_paths)
        self._load_image_with_objects(self.images_paths[self.currImgIdx])

    def _load_image_with_objects(self, file_path: str):
        """Load image with annotations.

        Parameters
        ----------
        file_path : str
            Path to the image.

        """
        objects = self.objects_map.get(file_path)
        self.canvas.load_image(file_path, objects)

    def update_objects_map(self):
        """Store current canvas objects for the current image."""
        current_path = self.images_paths[self.currImgIdx]
        if self.canvas.objects:
            self.objects_map[current_path] = self.canvas.objects


app = QApplication()

# stylesheet_path = Path(__file__).parent.parent / "assets" / "styles.qss"
# with open(stylesheet_path, "r") as f:
#     app.setStyleSheet(f.read())

window = MainWindow()
window.show()


if __name__ == "__main__":
    _ = app.exec()
