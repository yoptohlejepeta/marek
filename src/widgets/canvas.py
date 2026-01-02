from enum import StrEnum
import math
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QImage, QPainter, QPen, QColor, Qt, QBrush
from PySide6.QtCore import QPoint, QTimer, QPointF
from PySide6.QtGui import QPainterPath

CLOSE_THRESHOLD = 15
COLORS = [
    QColor(255, 0, 0),
    QColor(0, 255, 0),
    QColor(0, 0, 255),
    QColor(255, 255, 0),
    QColor(255, 0, 255),
]


class Tool(StrEnum):
    PEN = "pen"
    ERASER = "eraser"


class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.image = None
        self.zoom = 1.0
        self.offset = QPoint(0, 0)
        self.drawing = False
        self.current_points: list[QPoint] = []
        self.objects = []
        self.pan_start = QPoint(0, 0)
        self.tool: Tool = Tool.PEN

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMouseTracking(True)

    def load_image(self, file_path):
        self.image = QImage(file_path)
        self.zoom = 1.0
        self.offset = QPoint(0, 0)
        self.objects = []
        self.current_points = []
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
            self.zoom = min(zoom_x, zoom_y) * 0.9
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

        if not self.image:
            return

        scaled_image = self.image.scaledToWidth(
            int(self.image.width() * self.zoom),
            Qt.TransformationMode.SmoothTransformation,
        )
        painter.drawImage(self.offset, scaled_image)

        for i, obj in enumerate(self.objects):
            base_color = COLORS[i % len(COLORS)]

            painter.setPen(QPen(base_color, 2, Qt.PenStyle.SolidLine))

            fill_color = QColor(base_color)
            fill_color.setAlpha(100)
            painter.setBrush(QBrush(fill_color))

            self._draw_polygon(painter, obj, closed=True)

        if self.current_points:
            color = COLORS[len(self.objects) % len(COLORS)]
            painter.setPen(QPen(color, 2, Qt.PenStyle.SolidLine))

            self._draw_polygon(painter, self.current_points, closed=False)

    def _draw_polygon(self, painter, points, closed=True):
        if len(points) < 2:
            return

        screen_points = [self.screen_coords(p) for p in points]

        if closed and len(screen_points) >= 3:
            painter.drawPolygon(screen_points)
        else:
            painter.drawPolyline(screen_points)

    def _polygon_contains(self, polygon, point):
        path = QPainterPath()
        path.addPolygon([QPointF(p.x(), p.y()) for p in polygon])
        return path.contains(QPointF(point.x(), point.y()))

    def screen_coords(self, image_point):
        x = int(image_point.x() * self.zoom + self.offset.x())
        y = int(image_point.y() * self.zoom + self.offset.y())
        return QPoint(x, y)

    def wheelEvent(self, event):
        if not self.image:
            return

        zoom_factor = 1.1
        if event.angleDelta().y() > 0:
            self.zoom *= zoom_factor
        else:
            self.zoom /= zoom_factor

        self.zoom = max(0.1, min(self.zoom, 10.0))
        self.update()

    def mousePressEvent(self, event):
        if not self.image:
            return

        if event.button() == Qt.MouseButton.LeftButton:
            click_pos = self.image_coords(event.pos())

            match self.tool:
                case Tool.PEN:
                    self.drawing = True
                    if not self.current_points:
                        self.current_points = [click_pos]
                    else:
                        self.current_points.append(click_pos)
                case Tool.ERASER:
                    self.objects = [
                        obj
                        for obj in self.objects
                        if not self._polygon_contains(obj, click_pos)
                    ]
            self.update()

        elif event.button() == Qt.MouseButton.RightButton:
            self.pan_start = event.pos()

    def mouseMoveEvent(self, event):
        if not self.image:
            return

        if self.drawing and (event.buttons() & Qt.MouseButton.LeftButton):
            new_point = self.image_coords(event.pos())

            # Optimization: don't add point if it's identical to the last one
            if not self.current_points or self.current_points[-1] != new_point:
                self.current_points.append(new_point)
            self.update()

        elif event.buttons() & Qt.MouseButton.RightButton:
            delta = event.pos() - self.pan_start
            self.offset += delta
            self.pan_start = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if not self.image:
            return

        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False

            if len(self.current_points) >= 3:
                start = self.screen_coords(self.current_points[0])
                end = event.pos()
                distance = math.hypot(end.x() - start.x(), end.y() - start.y())

                if distance <= CLOSE_THRESHOLD:
                    self.objects.append(self.current_points)
                    self.current_points = []

            self.update()

    def image_coords(self, screen_point):
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

    def set_tool_pen(self):
        self.tool = Tool.PEN

    def set_tool_eraser(self):
        self.tool = Tool.ERASER

    def save(self): ...
