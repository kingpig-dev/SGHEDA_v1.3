import sys

from PyQt5.QtCore import Qt, QStandardPaths
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QLabel, QPushButton

from dashboardclass import Dashboard
from designclass import DesignClass
from EAHEdesignclass import EAHEDesignClass

def app_specific_path_sgheda():
    appdata_dir = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
    print("appdata_dir", appdata_dir)
    return appdata_dir + "/SGHEDA"

def app_specific_path_eahx():
    appdata_dir = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
    print("appdata_dir", appdata_dir)
    return appdata_dir + "/EAHX"

class Myapp(QMainWindow):
    def __init__(self, path1, path2):
        super().__init__()
        # self.setFixedSize(1210, 790)
        self.resize(1210, 790)
        self.setStyleSheet("background-color: #1F2843;")

        # Create a DesignClass
        self.design = DesignClass(self, path1)
        self.design.move(1000, 1000)

        # Create a EAGE class
        self.eahxdesign = EAHEDesignClass(self, path2)
        self.eahxdesign.move(1000, 1000)

        # Create a dashboard
        self.dashboard = Dashboard(self)

    def closeEvent(self, event):
        if self.design.btnexit():
            event.ignore()

    def designUI(self):
        print("designUI")
        self.dashboard.move(1000, 1000)
        self.design.move(0, 22)
        self.design.right_widget.setCurrentIndex(0)

    def eahx_designUI(self):
        print("eahx_designUI")
        self.dashboard.move(1000, 1000)
        self.eahxdesign.move(0, 22)
        self.design.right_widget.setCurrentIndex(0)

    def dashboardUI(self):
        print("dashboardUI")
        self.design.move(1000, 1000)
        self.eahxdesign.move(1000, 1000)
        self.dashboard.move(0, 0)

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        # self.setFixedHeight(100)
        self.resize(parent.width(), 23)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Title label
        self.title_label = QLabel("  SGHEDA (Slinky GHE Design & Analysis)")
        layout.addWidget(self.title_label)

        # Minimize button
        self.minimize_button = QPushButton("—")
        self.minimize_button.setFixedSize(34, 23)
        self.minimize_button.setStyleSheet('''
            QPushButton {
                border: none;
            }
            QPushButton:hover {
                background-color: #E5E5E5;
                color: white;
            }
        ''')
        self.minimize_button.clicked.connect(parent.showMinimized)
        layout.addWidget(self.minimize_button)

        # Close button
        self.close_button = QPushButton("X")
        self.close_button.setFixedSize(34, 23)
        self.close_button.setStyleSheet('''
            QPushButton {
                border: none;
            }
            QPushButton:hover {
                background-color: #E81123;
                color: white;
            }
        ''')
        self.close_button.clicked.connect(parent.close)
        layout.addWidget(self.close_button)

        # Set stylesheet for custom title bar
        self.setStyleSheet("""
            background-color: #F1F1F1;
            color: #ABABAB;
            font-weight: bold;
            font-size: 10px;
            text-align: center;
        """)

        # Set the title bar widget as the window's title bar
        self.parent().setWindowFlags(Qt.FramelessWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
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

if __name__ == '__main__':
    # Create a new QApplication instance
    appdata_dir_sgheda = app_specific_path_sgheda()
    appdata_dir_eahx = app_specific_path_eahx()
    app = QApplication(sys.argv)
    # Create a new MyApp instance
    my_app = Myapp(appdata_dir_sgheda, appdata_dir_eahx)

    titlebar = CustomTitleBar(my_app)
    # Show the main window
    my_app.show()

    # Start the event loop
    sys.exit(app.exec_())
