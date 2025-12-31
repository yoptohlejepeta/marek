from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QImage, QPainter, QPen, QColor, Qt
from PySide6.QtCore import QPoint, QRect


class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.image = None
        self.display_image = None
        self.zoom = 1.0
        self.offset = QPoint(0, 0)
        self.drawing = False
        self.last_point = QPoint()

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def load_image(self, file_path):
        self.image = QImage(file_path)
        self.display_image = self.image.copy()
        self.zoom = 1.0
        self.offset = QPoint(0, 0)
        self.fit_to_window()
        self.update()

    def fit_to_window(self):
        if not self.image:
            return

        window_width = self.width()
        window_height = self.height()
        img_width = self.image.width()
        img_height = self.image.height()

        if window_width > 0 and window_height > 0:
            zoom_x = window_width / img_width
            zoom_y = window_height / img_height
            self.zoom = min(zoom_x, zoom_y) * 0.9  # 90% to have some margin
            self.center_image()

    def center_image(self):
        if not self.image:
            return

        img_width = int(self.image.width() * self.zoom)
        img_height = int(self.image.height() * self.zoom)

        x = (self.width() - img_width) // 2
        y = (self.height() - img_height) // 2

        self.offset = QPoint(x, y)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(40, 40, 40))

        if not self.display_image:
            return

        # Draw scaled image
        scaled_image = self.display_image.scaledToWidth(
            int(self.display_image.width() * self.zoom),
            Qt.TransformationMode.SmoothTransformation,
        )

        painter.drawImage(self.offset, scaled_image)

    def wheelEvent(self, event):
        if not self.image:
            return

        # Zoom with scroll wheel
        zoom_factor = 1.1
        if event.angleDelta().y() > 0:
            self.zoom *= zoom_factor
        else:
            self.zoom /= zoom_factor

        self.zoom = max(0.1, min(self.zoom, 5.0))  # Clamp zoom
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.last_point = event.pos()
        elif event.button() == Qt.MouseButton.RightButton:
            # Start panning
            self.pan_start = event.pos()

    def mouseMoveEvent(self, event):
        if self.drawing and event.buttons() & Qt.MouseButton.LeftButton:
            # Draw line
            painter = QPainter(self.display_image)
            painter.setPen(QPen(QColor(255, 0, 0), 2, Qt.PenStyle.SolidLine))
            painter.drawLine(
                self.image_coords(self.last_point), self.image_coords(event.pos())
            )
            self.last_point = event.pos()
            self.update()
        elif event.buttons() & Qt.MouseButton.RightButton:
            # Pan
            delta = event.pos() - self.pan_start
            self.offset += delta
            self.pan_start = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False

    def image_coords(self, screen_point):
        """Convert screen coordinates to image coordinates"""
        if not self.image:
            return QPoint(0, 0)

        x = int((screen_point.x() - self.offset.x()) / self.zoom)
        y = int((screen_point.y() - self.offset.y()) / self.zoom)

        return QPoint(
            max(0, min(x, self.image.width() - 1)),
            max(0, min(y, self.image.height() - 1)),
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.image:
            self.fit_to_window()
