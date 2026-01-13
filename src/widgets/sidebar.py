from PySide6.QtWidgets import (
    QHBoxLayout,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
    QPushButton,
)
from PySide6.QtCore import Signal


class Sidebar(QWidget):
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
    nextImage = Signal()
    prevImage = Signal()

    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)

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

        toolsLayout = QHBoxLayout()

        handButton = QPushButton("✋ Hand")
        penButton = QPushButton("✏️ Pen")
        eraseButton = QPushButton("🧹 Eraser")
        saveButton = QPushButton("💾 Save")
        handButton.clicked.connect(self.hand.emit)
        penButton.clicked.connect(self.pen.emit)
        eraseButton.clicked.connect(self.eraser.emit)
        saveButton.clicked.connect(self.save.emit)
        toolsLayout.addWidget(handButton)
        toolsLayout.addWidget(penButton)
        toolsLayout.addWidget(eraseButton)
        toolsLayout.addWidget(saveButton)

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

        self.setMinimumWidth(100)
