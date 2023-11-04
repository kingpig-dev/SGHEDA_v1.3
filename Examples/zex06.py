from PyQt5 import QtWidgets, QtGui, QtCore


class CustomMessageBox(QtWidgets.QDialog):
    def __init__(self, icon, title, text, parent=None):
        super().__init__(parent)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # Set window icon
        self.setWindowIcon(icon)

        # Create layout
        layout = QtWidgets.QVBoxLayout()

        # Create icon label
        icon_label = QtWidgets.QLabel()
        icon_label.setPixmap(icon.pixmap(64, 64))
        layout.addWidget(icon_label)

        # Create text label
        text_label = QtWidgets.QLabel(text)
        layout.addWidget(text_label)

        # Create OK button
        ok_button = QtWidgets.QPushButton('OK')
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.setLayout(layout)


app = QtWidgets.QApplication([])

# Create icon
icon = QtGui.QIcon('path/to/icon.png')  # Replace with the path to your icon file

# Create and show the custom message box
custom_message_box = CustomMessageBox(icon, 'Custom Message', 'This is a custom message.')
custom_message_box.exec()

app.exec()