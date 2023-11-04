import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from buttonclass import MainButton
from labelclass import IntroLabel1, IntroLabel2

import os

def resource_path(relative_path):
    return os.path.join(relative_path)

class Dashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(1210, 790)

        # Set the background color of the main window
        self.setStyleSheet("background-color: #1F2843;")

        self.parent = parent

        # Set the window title
        self.setWindowTitle(resource_path('Slinky GHE Design & Analysis'))
        self.setWindowIcon(QIcon(resource_path("./Images/logo03_glowed.png")))

        # Add logo
        logo_pix = QPixmap(resource_path('./Images/logo03_glowed_white.png'))
        logo_pix.scaled(100, 100)
        logo_label = QLabel(self)
        logo_label.setPixmap(logo_pix.scaled(400, 300))
        logo_label.move(370, 100)

        # Add an introduction label
        intro_label_tile = IntroLabel1(self)
        intro_label_tile.setText('Welcome to Slinky GHE Design & Analysis!')
        intro_label_tile.move(350, 440)
        intro_label_tile.show()

        intro_label = IntroLabel2(self)
        intro_label.setText('''
           This tool's intuitive interface and user-friendly features make it accessible to both seasoned professionals and
         aspiring engineers. Its comprehensive analysis capabilities provide detailed insights into the performance of the GHE,
         allowing users to optimize design parameters, such as pipe spacing, size, and configuration, with unparalleled accuracy.
        This world-first slinky-type ground heat exchanger design and analysis tool represents the pinnacle of engineering ingenuity.
         With its unrivaled precision, ease of use, and commitment to sustainability, it empowers engineers and designers to unlock
            the full potential of geothermal energy, paving the way for a more efficient and environmentally friendly world.
        ''')
        intro_label.move(90, 490)
        intro_label.show()

        # Add a button to the layout
        design_button = MainButton(self)
        design_button.setText('Open Design && Analysis')
        design_button.show()
        design_button.move(450, 680)
        design_button.clicked.connect(self.designUI)

        # # Add another button to the layout
        # analysis_button = MainButton(self)
        # analysis_button.setText(self.tr('Design Analysis'))
        # analysis_button.show()
        # analysis_button.move(780, 650)
        # analysis_button.clicked.connect(self.analysisUI)

    def designUI(self):
        self.parent.designUI()

    def analysisUI(self):
        self.parent.analysisUI()


if __name__ == '__main__':
    # Create a new QApplication instance
    app = QApplication(sys.argv)

    # Create a new MyApp instance
    my_app = Dashboard()

    # Show the main window
    my_app.show()

    # Start the event loop
    sys.exit(app.exec_())
