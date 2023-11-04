import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QLabel, QHBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 500, 500)

        # Create the widgets
        self.lineEdit = QLineEdit()
        self.unitLabel = QLabel('mm')

        # Create a layout to hold the widgets
        layout = QHBoxLayout()
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.unitLabel)

        # Create a widget to hold the layout
        widget = QWidget()
        widget.setLayout(layout)

        # Set the widget as the central widget of the main window
        self.setCentralWidget(widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())