from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtCore, QtGui, QtWidgets


class IntroLabel1(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet('''
            QLabel {
                color: #7C8AA7;
                font-size: 30px;
                text-align: center;
            }
        ''')
        # self.setToolTip(text)  # Set the full text as a tooltip


class IntroLabel2(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet('''
            QLabel {
                color: #7C8AA7;
                font-size: 18px;
                text-align: center;
            }
        ''')

class IntroLabel3(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet('''
            QLabel {
                color: #7C8AA7;
                font-size: 18px;
                text-align: center;
                text-decoration: underline;
            }
        ''')

class ImageButton(QtWidgets.QPushButton):
    def __init__(self, parent, path):
        super().__init__(parent)
        self.icon = QtGui.QIcon(path)
        self.setIcon(self.icon)
        self.setIconSize(QSize(150, 130))

        self.setStyleSheet(
            """
        QPushButton{
            background-color: #1F2843;
            text-align: center;
            text-decoration: none;
            font-size: 20px;
            margin: 4px 2px;
            border: none;
        }
        """
        )
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.animation = QtCore.QPropertyAnimation(self, b"iconSize")
        self.animation.setDuration(300)  # Animation duration in milliseconds
        self.animation.setEasingCurve(QtCore.QEasingCurve.OutCubic)

    def enterEvent(self, event):
        self.animation.setEndValue(QtCore.QSize(165, 140))
        self.animation.start()

    def leaveEvent(self, event):
        self.animation.setEndValue(QtCore.QSize(150, 130))
        self.animation.start()


# if __name__ == "__main__":
#     import sys
#
#     app = QtWidgets.QApplication(sys.argv)
#     w = Dialog()
#     w.show()
#     sys.exit(app.exec_())
