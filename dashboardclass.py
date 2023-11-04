import sys
import webbrowser

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from buttonclass import MainButton
from labelclass import IntroLabel1, IntroLabel2, IntroLabel4

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
        logo_label.setPixmap(logo_pix.scaled(430, 350))
        logo_label.move(630, 200)

        # Add another button to the layout
        website_button = MainButton(self)
        website_button.setText(self.tr('Open Website'))
        website_button.setToolTip("https://slinkyghxdesign.com")
        website_button.show()
        website_button.setCursor(Qt.DragLinkCursor)
        website_button.clicked.connect(self.redirect_to_website)
        website_button.move(810, 600)

        # Add an introduction label
        intro_label_tile = IntroLabel1(self)
        intro_label_tile.setText('Welcome to')
        intro_label_tile.move(100, 130)
        intro_label_tile.show()

        intro_label_tile = IntroLabel1(self)
        intro_label_tile.setText('Slinky GHE Design & Analysis!')
        intro_label_tile.move(100, 180)
        intro_label_tile.show()

        feature_label1 = IntroLabel2(self)
        feature_label1.setText('✓ Comprehensive Design Capabilities')
        feature_label1.move(120, 360)

        feature_label2 = IntroLabel2(self)
        feature_label2.setText('✓ Accurate Performance Analysis')
        feature_label2.move(120, 420)

        feature_label2 = IntroLabel2(self)
        feature_label2.setText('✓ User-friendly Interface')
        feature_label2.move(120, 480)

        # Add a button to the layout
        design_button = MainButton(self)
        design_button.setText('Open Program')
        design_button.show()
        design_button.move(200, 600)
        design_button.clicked.connect(self.designUI)

        copyright_label = IntroLabel4(self)
        copyright_label.setText('''
                                                                                         Copyright © 2023 SGHEDA
            Warning: This program is protected by copyright law and international treaties. Unauthorized reproduction or distribution of this program,
                    or any portion of it, may result in severe civil and criminal penalties, and will be prosecuted to the maximum extent under law.
        ''')
        copyright_label.move(140, 700)

    def designUI(self):
        self.parent.designUI()

    def analysisUI(self):
        self.parent.analysisUI()

    def redirect_to_website(self):
        webbrowser.open("https://slinkyghxdesign.com")

if __name__ == '__main__':
    # Create a new QApplication instance
    app = QApplication(sys.argv)

    # Create a new MyApp instance
    my_app = Dashboard()

    # Show the main window
    my_app.show()

    # Start the event loop
    sys.exit(app.exec_())
