from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QLabel, QPushButton


class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        # self.setFixedHeight(100)
        self.resize(400, 30)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Title label
        self.title_label = QLabel("Custom Title Bar")
        layout.addWidget(self.title_label)

        # Minimize button
        self.minimize_button = QPushButton("-")
        self.minimize_button.clicked.connect(self.parent().showMinimized)
        layout.addWidget(self.minimize_button)

        # Close button
        self.close_button = QPushButton("X")
        self.close_button.clicked.connect(self.parent().close)
        layout.addWidget(self.close_button)

        # Set stylesheet for custom title bar
        self.setStyleSheet("""
            background-color: #333333;
            color: #FFFFFF;
            font-weight: bold;
            padding-left: 8px;
        """)

        # Set the title bar widget as the window's title bar
        self.parent().setWindowFlags(Qt.FramelessWindowHint)
        # self.parent().setWindowTitle("Custom Title Bar")
        # self.parent().layout().setContentsMargins(0, self.height(), 0, 0)
        self.parent().layout().addWidget(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent().drag_position = event.globalPos() - self.parent().frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.parent().move(event.globalPos() - self.parent().drag_position)
            event.accept()


if __name__ == "__main__":
    app = QApplication([])

    # Create a main window
    window = QMainWindow()
    window.resize(400, 300)

    # Create a custom title bar widget
    title_bar = CustomTitleBar(window)

    # Add some content to the window
    # content_widget = QWidget()
    # window.setCentralWidget(content_widget)

    # Show the window
    window.show()

    # Start the application event loop
    app.exec_()