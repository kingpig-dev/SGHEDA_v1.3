import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton


class Notification(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Notification")
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setText("Are you sure you want to exit?")
        self.setIcon(QMessageBox.Question)

        # Customize the buttons
        yes_button = self.addButton(QMessageBox.Yes)
        no_button = self.addButton(QMessageBox.No)

        # Apply custom styles to the buttons
        yes_button.setStyleSheet(
            """
                QPushButton{
                    background-color: #333A51;
                    color: white;
                    border-radius: 10px;
                    text-align: center;
                    text-decoration: none;
                    font-size: 16px;
                    margin: 4px 2px;
                    border: 2px solid #6B963B;
                    width: 80px;
                }
                QPushButton:hover {
                    background-color: #5D7C4C;
                }
            """
        )
        no_button.setStyleSheet(
            """
                QPushButton{
                    background-color: #333A51;
                    color: white;
                    border-radius: 10px;
                    text-align: center;
                    text-decoration: none;
                    font-size: 16px;
                    margin: 4px 2px;
                    border: 2px solid #C03647;
                    width: 80px;
                }
                QPushButton:hover {
                    background-color: #943A4C;
                }
            """
        )

        self.setDefaultButton(QMessageBox.No)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Exit Button with Customized Notification")
        self.setGeometry(100, 100, 400, 300)

        # Create the exit button
        exit_button = QPushButton("Exit", self)
        exit_button.clicked.connect(self.show_exit_notification)
        exit_button.setGeometry(150, 120, 100, 30)

    def show_exit_notification(self):
        notification = Notification(self)
        result = notification.exec_()

        if result == QMessageBox.Yes:
            # Perform exit actions or close the application
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())