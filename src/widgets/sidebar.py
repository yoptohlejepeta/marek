from PySide6.QtWidgets import QVBoxLayout, QWidget, QSizePolicy, QPushButton
from PySide6.QtCore import Signal


class Sidebar(QWidget):
    open_image_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)

        sidebarLayout = QVBoxLayout()
        sidebarLayout.setContentsMargins(5, 5, 5, 5)
        sidebarLayout.setSpacing(5)

        open_btn = QPushButton("Open Image")
        open_btn.clicked.connect(self.open_image_clicked.emit)
        sidebarLayout.addWidget(open_btn)

        sidebarLayout.addStretch()

        sidebarLayout.addWidget(QPushButton("✏️ Pen"))
        sidebarLayout.addWidget(QPushButton("🧹 Eraser"))
        sidebarLayout.addWidget(QPushButton("💾 Save"))

        self.setLayout(sidebarLayout)

        self.setMinimumWidth(100)
