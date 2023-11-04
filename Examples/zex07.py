import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QGridLayout()
        layout.addWidget(QPushButton("Button 1"), 0, 0)
        layout.addWidget(QPushButton("Button 2"), 0, 1)
        layout.addWidget(QPushButton("Button 3"), 0, 2)
        layout.addWidget(QPushButton("Button 4"), 1, 0)
        layout.addWidget(QPushButton("Button 5"), 1, 1)
        layout.addWidget(QPushButton("Button 6"), 1, 2)

        # Span 3 columns for Button 2
        layout.addWidget(QPushButton("Spanning Button"), 0, 1, 1, 3)

        # Set alignment to center
        layout.setAlignment(layout, Qt.AlignCenter)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())