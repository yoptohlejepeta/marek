import logging
import sys

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
)

from widgets.bottombar import BottomBar
from widgets.canvas import Canvas
from widgets.toolbar import ToolBar


def exception_hook(exc_type, exc_value, exc_traceback):
    logging.error("Unhandled exception:", exc_info=(exc_type, exc_value, exc_traceback))
    sys.__excepthook__(exc_type, exc_value, exc_traceback)


sys.excepthook = exception_hook


class MainWindow(QMainWindow):
    imagesPaths: list[str] = []
    currImgIdx: int = 0
    objects_map: dict[str, list] = {}

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MAReK")
        self.setGeometry(100, 100, 1200, 800)

        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)

        self.toolbar = ToolBar(self.canvas)
        self.bottom_bar = BottomBar(self.canvas)

        self.bottom_bar.open_image_clicked.connect(self.open_images)
        self.toolbar.hand.connect(self.canvas.set_tool_hand)
        self.toolbar.pen.connect(self.canvas.set_tool_pen)
        self.toolbar.eraser.connect(self.canvas.set_tool_eraser)
        self.toolbar.save.connect(self.canvas.save)
        self.bottom_bar.nextImage.connect(self.next_image)
        self.bottom_bar.prevImage.connect(self.prev_image)
        self.canvas.objects_updated.connect(self.update_objects_map)

        self.toolbar.show()
        self.bottom_bar.show()

        self._position_floating_panels()

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
            self.bottom_bar.update_counter(self.currImgIdx, len(self.images_paths))

    def next_image(self):
        self.currImgIdx = (self.currImgIdx + 1) % len(self.images_paths)
        self._load_image_with_objects(self.images_paths[self.currImgIdx])
        self.bottom_bar.update_counter(self.currImgIdx, len(self.images_paths))

    def prev_image(self):
        self.currImgIdx = (self.currImgIdx - 1) % len(self.images_paths)
        self._load_image_with_objects(self.images_paths[self.currImgIdx])
        self.bottom_bar.update_counter(self.currImgIdx, len(self.images_paths))

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

    def _position_floating_panels(self):
        """Position floating panels on the canvas."""
        canvas_width = self.canvas.width()
        canvas_height = self.canvas.height()

        toolbar_width = self.toolbar.width()
        toolbar_height = self.toolbar.height()
        toolbar_x = canvas_width - toolbar_width - 20
        toolbar_y = (canvas_height - toolbar_height) // 2
        self.toolbar.move(toolbar_x, toolbar_y)
        self.toolbar.raise_()

        bottom_width = self.bottom_bar.width()
        bottom_height = self.bottom_bar.height()
        bottom_x = (canvas_width - bottom_width) // 2
        bottom_y = canvas_height - bottom_height - 20
        self.bottom_bar.move(bottom_x, bottom_y)
        self.bottom_bar.raise_()

    def resizeEvent(self, event):
        """Reposition floating panels when window is resized."""
        super().resizeEvent(event)
        self._position_floating_panels()

    def moveEvent(self, event):
        """Reposition floating panels when window is moved."""
        super().moveEvent(event)
        self._position_floating_panels()


app = QApplication()

# stylesheet_path = Path(__file__).parent.parent / "assets" / "styles.qss"
# with open(stylesheet_path, "r") as f:
#     app.setStyleSheet(f.read())

window = MainWindow()
window.show()


if __name__ == "__main__":
    _ = app.exec()
