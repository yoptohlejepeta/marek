from PySide6.QtWidgets import (
    QHBoxLayout,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QMessageBox,
)
from PySide6.QtCore import Signal


class ToolBar(QWidget):
    """
    Attributes
    ----------
    open_image_clicked : open image signal
    pen : pen mode
    eraser : eraser mode
    save : save current objects
    """

    open_image_clicked = Signal()
    hand = Signal()
    pen = Signal()
    eraser = Signal()
    save = Signal()
    save_success = Signal(str)  # Emit success message
    nextImage = Signal()
    prevImage = Signal()

    def __init__(self):
        super().__init__()
        # self.setAutoFillBackground(True)

        self.selected_tool = None

        sidebarLayout = QVBoxLayout()
        sidebarLayout.setContentsMargins(5, 5, 5, 5)
        sidebarLayout.setSpacing(5)

        imageButtonLayout = QHBoxLayout()

        fileButton = QPushButton("Open Images")
        fileButton.clicked.connect(self.open_image_clicked.emit)
        imageButtonLayout.addWidget(fileButton)

        sidebarLayout.addLayout(imageButtonLayout)

        vSpace = QSpacerItem(1, 50)
        sidebarLayout.addSpacerItem(vSpace)

        toolsLayout = QVBoxLayout()

        self.handButton = QPushButton("✋ Hand")
        self.penButton = QPushButton("✏️ Pen")
        self.eraseButton = QPushButton("🧹 Eraser")
        self.saveButton = QPushButton("💾 Save")
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

        sidebarLayout.addLayout(toolsLayout)

        sidebarLayout.addStretch()

        nextPrevLayout = QHBoxLayout()
        nextButton = QPushButton("➡️")
        prevButton = QPushButton("⬅️")
        nextButton.clicked.connect(self.nextImage.emit)
        prevButton.clicked.connect(self.prevImage.emit)
        nextPrevLayout.addWidget(prevButton)
        nextPrevLayout.addWidget(nextButton)

        sidebarLayout.addLayout(nextPrevLayout)

        self.setLayout(sidebarLayout)
        self._set_button_highlight(self.handButton)

        self.setMinimumWidth(100)

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
