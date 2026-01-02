from PySide6.QtWidgets import (
    QHBoxLayout,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
    QPushButton,
)
from PySide6.QtCore import Signal


class Sidebar(QWidget):
    open_image_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)

        sidebarLayout = QVBoxLayout()
        sidebarLayout.setContentsMargins(5, 5, 5, 5)
        sidebarLayout.setSpacing(5)

        imageButtonLayout = QHBoxLayout()

        fileButton = QPushButton("Open Image")
        fileButton.clicked.connect(self.open_image_clicked.emit)
        imageButtonLayout.addWidget(fileButton)

        filesButton = QPushButton("Open Images")
        imageButtonLayout.addWidget(filesButton)

        sidebarLayout.addLayout(imageButtonLayout)

        # sidebarLayout.addStretch()
        vSpace = QSpacerItem(1, 50)
        sidebarLayout.addSpacerItem(vSpace)

        toolsLayout = QHBoxLayout()

        toolsLayout.addWidget(QPushButton("✏️ Pen"))
        toolsLayout.addWidget(QPushButton("🧹 Eraser"))
        toolsLayout.addWidget(QPushButton("💾 Save"))

        sidebarLayout.addLayout(toolsLayout)

        sidebarLayout.addStretch()

        self.setLayout(sidebarLayout)

        self.setMinimumWidth(100)
