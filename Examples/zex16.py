import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QRadioButton, QGroupBox, QLabel, QLineEdit


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Radio Buttons Example')
        self.setGeometry(300, 300, 300, 200)

        vbox = QVBoxLayout()
        groupbox = QGroupBox('Options')

        radio1 = QRadioButton('Option 1')
        radio2 = QRadioButton('Option 2')

        vbox.addWidget(radio1)
        vbox.addWidget(radio2)

        groupbox.setLayout(vbox)

        self.label1 = QLabel('Label 1')
        self.lineedit1 = QLineEdit()
        self.label2 = QLabel('Label 2')
        self.lineedit2 = QLineEdit()

        vbox = QVBoxLayout()
        vbox.addWidget(groupbox)
        vbox.addWidget(self.label1)
        vbox.addWidget(self.lineedit1)
        vbox.addWidget(self.label2)
        vbox.addWidget(self.lineedit2)

        self.setLayout(vbox)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec_())