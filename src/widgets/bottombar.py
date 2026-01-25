from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
)


class BottomBar(QWidget):
    """Floating bottom bar with image navigation and counter."""

    open_image_clicked = Signal()
    nextImage = Signal()
    prevImage = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(5)

        font = QFont()
        font.setPointSize(16)

        prevButton = QPushButton("⬅️")
        prevButton.setMinimumWidth(60)
        prevButton.setMinimumHeight(45)
        prevButton.setMaximumWidth(60)
        prevButton.setMaximumHeight(45)
        prevButton.setFont(font)
        prevButton.clicked.connect(self.prevImage.emit)
        layout.addWidget(prevButton)

        layout.addSpacing(10)

        self.counterLabel = QLabel("No images loaded")
        self.counterLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.counterLabel.setMinimumWidth(140)
        layout.addWidget(self.counterLabel)

        layout.addSpacing(10)

        openButton = QPushButton("📁")
        openButton.setMinimumWidth(60)
        openButton.setMinimumHeight(45)
        openButton.setMaximumWidth(60)
        openButton.setMaximumHeight(45)
        openButton.setFont(font)
        openButton.clicked.connect(self.open_image_clicked.emit)
        layout.addWidget(openButton)

        layout.addSpacing(10)

        nextButton = QPushButton("➡️")
        nextButton.setMinimumWidth(60)
        nextButton.setMinimumHeight(45)
        nextButton.setMaximumWidth(60)
        nextButton.setMaximumHeight(45)
        nextButton.setFont(font)
        nextButton.clicked.connect(self.nextImage.emit)
        layout.addWidget(nextButton)

        self.setLayout(layout)
        self.setMinimumHeight(50)
        self.setMaximumHeight(50)
        self.adjustSize()

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(220, 224, 232, 200))
        self.setPalette(palette)

    def update_counter(self, current: int, total: int):
        """Update the image counter display."""
        if total == 0:
            self.counterLabel.setText("No images loaded")
        else:
            self.counterLabel.setText(f"Image {current + 1} of {total}")
