from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtCore, QtGui, QtWidgets


class IntroLabel1(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet('''
            QLabel {
                color: #7C8AA7;
                font-size: 35px;
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
                font-size: 25px;
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
class IntroLabel4(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet('''
            QLabel {
                color: #7C8AA7;
                font-size: 14px;
                text-align: center;
            }
        ''')

class TickerLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet('''
            QLabel {
                background-color: rgba(0,0,0,0);
                color: #7C8AA7;
                font-size: 18px;
                text-align: center;
            }
        ''')
        self.setPixmap(QPixmap('./Images/tick07.png').scaled(25, 25))


class Dialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(self.tr("Dialog"))

        self.intro_label = IntroLabel1(self)
        self.intro_label.setText(self.tr("Click Here"))
        self.intro_label.move(50, 50)
        self.intro_label.show()

        self.ticker_label = TickerLabel(self)
        self.ticker_label.move(200, 50)
        # self.ticker_label.show()
        self.resize(400, 300)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Dialog()
    w.show()
    sys.exit(app.exec_())
