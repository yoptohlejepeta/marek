from PySide6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QMessageBox,
    QLabel,
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QColor, QPalette, QFont


class ToolBar(QWidget):
    """Floating toolbar on the right with tools only."""

    hand = Signal()
    pen = Signal()
    eraser = Signal()
    save = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.selected_tool = None

        toolsLayout = QVBoxLayout()
        toolsLayout.setContentsMargins(3, 3, 3, 3)
        toolsLayout.setSpacing(2)

        self.handButton = QPushButton("✋")
        self.penButton = QPushButton("✏️")
        self.eraseButton = QPushButton("🧹")
        self.saveButton = QPushButton("💾")

        font = QFont()
        font.setPointSize(20)
        for btn in [self.handButton, self.penButton, self.eraseButton, self.saveButton]:
            btn.setMinimumWidth(70)
            btn.setMinimumHeight(70)
            btn.setMaximumWidth(70)
            btn.setMaximumHeight(70)
            btn.setFont(font)

        self.handButton.clicked.connect(self._on_hand_clicked)
        self.penButton.clicked.connect(self._on_pen_clicked)
        self.eraseButton.clicked.connect(self._on_eraser_clicked)
        self.saveButton.clicked.connect(self._on_save_clicked)

        toolsLayout.addWidget(self.handButton)
        toolsLayout.addWidget(self.penButton)
        toolsLayout.addWidget(self.eraseButton)
        toolsLayout.addWidget(self.saveButton)

        self._highlight_style = "background-color: #4CAF50; font-weight: bold;"
        self._normal_style = ""

        self.setLayout(toolsLayout)
        self._set_button_highlight(self.handButton)

        self.setMinimumWidth(90)
        self.setMaximumWidth(90)
        self.adjustSize()

    def _set_button_highlight(self, button):
        """Highlight the selected tool button"""
        if self.selected_tool:
            self.selected_tool.setStyleSheet(self._normal_style)

        button.setStyleSheet(self._highlight_style)
        self.selected_tool = button

    def _on_hand_clicked(self):
        self._set_button_highlight(self.handButton)
        self.hand.emit()

    def _on_pen_clicked(self):
        self._set_button_highlight(self.penButton)
        self.pen.emit()

    def _on_eraser_clicked(self):
        self._set_button_highlight(self.eraseButton)
        self.eraser.emit()

    def _on_save_clicked(self):
        self.save.emit()
        QMessageBox.information(self, "Success", "Saved successfully!")


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
