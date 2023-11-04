import sys
import webbrowser

from PyQt5.QtCore import Qt

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from buttonclass import ImageButton, ImageButton2
from labelclass import IntroLabel3

import traceback
import os


def resource_path(relative_path):
    return os.path.join(relative_path)


class InputForm(QGroupBox):

    def __init__(self, parent, elements, design):
        super().__init__(parent)
        self.design = design
        self.setStyleSheet('''
            * {
                background-color: #1F2843;
                color: white;
                font-size: 16px;
                padding: 5px 10px;
            }
            
            QGroupBox {
                border: 1px solid white;
                border-radius: 30%;
            }
        ''')

        self.elements = elements
        self.grid = QGridLayout(self)
        label_title = IntroLabel3(elements[0])
        label_title.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(label_title, 1, 0, 1, 3)
        self.input = []

        for i in range(1, len(elements)):
            if elements[i][2] == 'lineedit':
                # name
                a = QLabel(elements[i][0])
                a.setStyleSheet('''
                    QLabel {
                        text-align: center;
                    }
                ''')

                # input data
                b = QLineEdit()
                b.setValidator(QDoubleValidator())
                b.setMaxLength(10)
                b.setStyleSheet('''
                    QLineEdit {
                        text-align: center;
                        background-color: #1F2843;
                        color: white;
                        border: none;
                        border-bottom: 2px solid #1F8EFA;
                    }
                ''')
                if self.design.value_default_data:
                    b.setText(elements[i][3])
                else:
                    b.setPlaceholderText(elements[i][3])

                b.setAlignment(Qt.AlignCenter)

                # unit
                c = QLabel(elements[i][1])
                self.grid.addWidget(a, i + 1, 0)
                self.grid.addWidget(b, i + 1, 1)
                self.grid.addWidget(c, i + 1, 2)
                self.input.append(b)

            elif elements[i][2] == 'combobox':

                a = QLabel(elements[i][0])
                b = QComboBox()
                b.addItems(elements[i][1])
                b.setStyleSheet("""            
                     QComboBox {
                        background-color: #2C3751;
                        selection-background-color: #555555;
                        min-width: 2em;
                        font-size: 16px;
                        text-align: center;
                    }
                    
                    QComboBox::hover{
                        color: #2978FA
                    }
                    
                    QComboBox::drop-down {
                        subcontrol-origin: padding;
                        width: 25px;
                        border: none;
                    }
                    
                    QComboBox::down-arrow {
                        border: 0px;
                        background-image-width: 30px;
                        border-image: url(./Images/down.png);
                    }
                """)

                self.grid.addWidget(a, i + 1, 0)
                self.grid.addWidget(b, i + 1, 1, 1, 2)
                self.input.append(b)

        # self.btn_next = QPushButton()
        # self.btn_next.setText("Next")
        # self.btn_next.clicked.connect(self.btnnext)
        # self.grid.addWidget(self.btn_next, 5, 1)
        self.grid.setAlignment(Qt.AlignCenter)
        self.setLayout(self.grid)

    def btnnext(self):
        if self.getValidation():
            self.getData()

    def getData(self):
        dict = {}
        for i in range(1, len(self.input) + 1):
            # print(self.elements[i][2], i)
            if self.elements[i][2] == "lineedit":
                dict[self.elements[i][0]] = self.input[i - 1].text()
                print(self.input[i - 1].text())
            elif self.elements[i][2] == "combobox":
                dict[self.elements[i][0]] = self.input[i - 1].currentText()
                print(self.input[i - 1].currentText())
        return dict

    def getValidation(self):
        for i in range(1, len(self.input) + 1):
            if self.elements[i][2] == "lineedit":
                if self.input[i - 1].text() == "":
                    return False
        return True

    def setData(self, data):
        print('setData')
        try:
            for i in range(1, len(self.input) + 1):
                if self.elements[i][2] == "lineedit":
                    self.input[i - 1].setText(data[i][3])
                else:
                    self.input[i - 1].setCurrentText(data[i][2])
        except Exception as e:
            print('setData expeption: ', traceback.format_exc())

    def setData1(self, data):
        print(data)
        try:
            for i in range(1, len(self.input) + 1):
                if self.elements[i][2] == "lineedit":
                    self.input[i - 1].setText(data[i - 1])
                else:
                    self.input[i - 1].setCurrentText(data[i - 1])
        except Exception as e:
            print("setData exception: ", traceback.format_exc())
            # print(i)

    def setReadOnly(self, data):
        for i in range(1, len(self.input) + 1):
            self.input[i - 1].setReadOnly(data)


class DesignInputForm(QGroupBox):

    def __init__(self, parent, elements, design):
        super().__init__(parent)
        self.design = design
        self.setStyleSheet('''
            * {
                background-color: #1F2843;
                color: white;
                font-size: 16px;
                padding: 5px 10px;
            }

            QGroupBox {
                border: 1px solid white;
                border-radius: 30%;
            }
        ''')

        self.elements = elements
        self.grid = QGridLayout(self)
        label_title = IntroLabel3(elements[0])
        label_title.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(label_title, 1, 0, 1, 3)
        self.input = []

        for i in range(1, len(elements)):
            if elements[i][2] == 'lineedit':
                # name
                a = QLabel(elements[i][0])
                a.setStyleSheet('''
                    QLabel {
                        text-align: center;
                    }
                ''')

                # input data
                b = QLineEdit()
                b.setValidator(QDoubleValidator())
                b.setMaxLength(10)
                b.setStyleSheet('''
                    QLineEdit {
                        text-align: center;
                        background-color: #1F2843;
                        color: white;
                        border: none;
                        border-bottom: 2px solid #1F8EFA;
                    }
                ''')

                b.setPlaceholderText(elements[i][3])

                b.setAlignment(Qt.AlignCenter)

                # unit
                c = QLabel(elements[i][1])
                self.grid.addWidget(a, i + 1, 0)
                self.grid.addWidget(b, i + 1, 1)
                self.grid.addWidget(c, i + 1, 2)
                self.input.append(b)

            elif elements[i][2] == 'combobox':

                a = QLabel(elements[i][0])
                b = QComboBox()
                b.addItems(elements[i][1])
                b.setStyleSheet("""            
                     QComboBox {
                        background-color: #2C3751;
                        selection-background-color: #555555;
                        min-width: 2em;
                        font-size: 16px;
                        text-align: center;
                    }

                    QComboBox::hover{
                        color: #2978FA
                    }

                    QComboBox::drop-down {
                        subcontrol-origin: padding;
                        width: 25px;
                        border: none;
                    }

                    QComboBox::down-arrow {
                        border: 0px;
                        background-image-width: 30px;
                        border-image: url(./Images/down.png);
                    }
                """)

                self.grid.addWidget(a, i + 1, 0)
                self.grid.addWidget(b, i + 1, 1, 1, 2)
                self.input.append(b)

        # self.btn_next = QPushButton()
        # self.btn_next.setText("Next")
        # self.btn_next.clicked.connect(self.btnnext)
        # self.grid.addWidget(self.btn_next, 5, 1)
        self.grid.setAlignment(Qt.AlignCenter)
        self.setLayout(self.grid)

    def btnnext(self):
        if self.getValidation():
            self.getData()

    def getData(self):
        dict = {}
        for i in range(1, len(self.input) + 1):
            # print(self.elements[i][2], i)
            if self.elements[i][2] == "lineedit":
                dict[self.elements[i][0]] = self.input[i - 1].text()
                print(self.input[i - 1].text())
            elif self.elements[i][2] == "combobox":
                dict[self.elements[i][0]] = self.input[i - 1].currentText()
                print(self.input[i - 1].currentText())
        return dict

    def getValidation(self):
        for i in range(1, len(self.input) + 1):
            if self.elements[i][2] == "lineedit":
                if self.input[i - 1].text() == "":
                    return False
        return True

    def setData(self, data):
        print('setData')
        try:
            for i in range(1, len(self.input) + 1):
                if self.elements[i][2] == "lineedit":
                    self.input[i - 1].setText(data[i][3])
                else:
                    self.input[i - 1].setCurrentText(data[i][2])
        except Exception as e:
            print('setData expeption: ', traceback.format_exc())

    def setData1(self, data):
        print(data)
        try:
            for i in range(1, len(self.input) + 1):
                if self.elements[i][2] == "lineedit":
                    self.input[i - 1].setText(data[i - 1])
                else:
                    self.input[i - 1].setCurrentText(data[i - 1])
        except Exception as e:
            print("setData exception: ", traceback.format_exc())
            # print(i)

    def setReadOnly(self, data):
        for i in range(1, len(self.input) + 1):
            self.input[i - 1].setReadOnly(data)


class Pipe_InputForm(QGroupBox):

    def __init__(self, parent, elements, design):
        super().__init__(parent)
        self.design = design
        self.setStyleSheet('''
            * {
                background-color: #1F2843;
                color: white;
                font-size: 16px;
                padding: 5px 10px;
            }

            QGroupBox {
                border: 1px solid white;
                border-radius: 30%;
            }
        ''')
        self.elements = elements
        self.grid = QGridLayout(self)
        label_title = IntroLabel3(elements[0])
        label_title.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(label_title, 1, 0, 1, 3)
        self.input = []
        for i in range(1, len(elements)):
            if elements[i][2] == 'lineedit':
                a = QLabel(elements[i][0])
                a.setStyleSheet('''
                    QLabel {
                        text-align: center;
                    }
                ''')
                b = QLineEdit()
                b.setValidator(QDoubleValidator())
                b.setMaxLength(10)
                b.setStyleSheet('''
                    QLineEdit {
                        text-align: center;
                        background-color: #1F2843;
                        color: white;
                        border: none;
                        border-bottom: 2px solid #1F8EFA;
                    }
                ''')
                b.setText(elements[i][3])
                b.setAlignment(Qt.AlignCenter)


                c = QLabel(elements[i][1])
                self.grid.addWidget(a, i + 1, 0)
                self.grid.addWidget(b, i + 1, 1)
                self.grid.addWidget(c, i + 1, 2)
                self.input.append(b)

            elif elements[i][2] == 'combobox':

                a = QLabel(elements[i][0])
                b = QComboBox()
                b.addItems(elements[i][1])
                b.setStyleSheet("""            
                     QComboBox {
                        background-color: #2C3751;
                        selection-background-color: #555555;
                        min-width: 2em;
                        font-size: 16px;
                        text-align: center;
                    }

                    QComboBox::hover{
                        color: #2978FA
                    }

                    QComboBox::drop-down {
                        subcontrol-origin: padding;
                        width: 25px;
                        border: none;
                    }

                    QComboBox::down-arrow {
                        border: 0px;
                        background-image-width: 30px;
                        border-image: url(./Images/down.png);
                    }
                """)

                self.grid.addWidget(a, i + 1, 0)
                self.grid.addWidget(b, i + 1, 1, 1, 2)
                self.input.append(b)

        # self.btn_next = QPushButton()
        # self.btn_next.setText("Next")
        # self.btn_next.clicked.connect(self.btnnext)
        # self.grid.addWidget(self.btn_next, 5, 1)
        self.grid.setAlignment(Qt.AlignCenter)
        self.setLayout(self.grid)

    def btnnext(self):
        if self.getValidation():
            self.getData()

    def getData(self):
        dict = {}
        for i in range(1, len(self.input) + 1):
            # print(self.elements[i][2], i)
            if self.elements[i][2] == "lineedit":
                dict[self.elements[i][0]] = self.input[i - 1].text()
                print(self.input[i - 1].text())
            elif self.elements[i][2] == "combobox":
                dict[self.elements[i][0]] = self.input[i - 1].currentText()
                print(self.input[i - 1].currentText())
        return dict

    def getValidation(self):
        for i in range(1, len(self.input) + 1):
            if self.elements[i][2] == "lineedit":
                if self.input[i - 1].text() == "":
                    return False
        return True

    def setData(self, data):
        print('setData')
        try:
            for i in range(1, len(self.input) + 1):
                if self.elements[i][2] == "lineedit":
                    self.input[i - 1].setText(data[i][3])
                else:
                    self.input[i - 1].setCurrentText(data[i][2])
        except Exception as e:
            print('setData expeption: ', traceback.format_exc())

    def setData1(self, data):
        # print(data)
        # i=0
        try:
            for i in range(1, len(self.input) + 1):
                if self.elements[i][2] == "lineedit":
                    self.input[i - 1].setText(data[i - 1])
                else:
                    self.input[i - 1].setCurrentText(data[i - 1])
        except Exception as e:
            print("setData exception: ", traceback.format_exc())
            # print(i)

    def setReadOnly(self, data):
        for i in range(1, len(self.input) + 1):
            self.input[i - 1].setReadOnly(data)

    def setPipeSize(self):
        self.design.update_pipe()


class InputDescription(QWidget):
    def __init__(self, parent, elements):
        super().__init__(parent)
        self.setStyleSheet('''
            background-color: #1F2843;
            color: white;
            font-size: 16px;
            padding: 5px 10px;
            QWidget {
                border: 2px solid red;
            }
        ''')
        self.elements = elements
        self.grid = QGridLayout(self)
        label_title = IntroLabel3(elements[0])
        label_title.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(label_title, 1, 0)

        self.description = CustomQTextEdit(self)
        self.description.setText(elements[1])
        self.grid.addWidget(self.description, 2, 0)

    def getData(self):
        return self.description.toPlainText()

    def getValidation(self):
        if self.description.toPlainText() == '':
            return False
        else:
            return True


class CustomQTextEdit(QTextEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet("""
            background-color: #2C3751;
            color: #7C8AA7;
            font-size: 16px;
            padding: 10px 20px 10px 20px;
            border-radius: 10px solid white;
        """)


class LicenseForm(QGroupBox):
    def __init__(self, parent, design):
        super().__init__(parent)
        self.parent = parent
        self.design = design
        self.value_machinenumber = self.design.get_machine_number()
        self.setStyleSheet('''
            * {
                background-color: #1F2843;
                color: white;
                font-size: 16px;
                padding: 5px 10px;
            }
            
            QGroupBox {
                border: 1px solid white;
                border-radius: 30%;
            }
        ''')

        self.grid = QGridLayout(self)

        self.label_title = IntroLabel3('License Information')
        self.label_title.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.label_title, 1, 1, 1, 2)

        self.label_machinenumber = QLabel('Machine Number')
        self.label_machinenumber.setStyleSheet('''
                    QLabel {
                        text-align: center;
                    }
                ''')
        self.machinenumber = QLineEdit(self)
        self.machinenumber.setAlignment(Qt.AlignCenter)
        self.machinenumber.setStyleSheet('''
                            QLineEdit {
                                text-align: center;
                                background-color: #1F2843;
                                border: none;
                                border-bottom: 2px solid #1F8EFA;
                            }
                        ''')
        self.machinenumber.setText(self.value_machinenumber)

        self.grid.addWidget(self.label_machinenumber, 2, 1)
        self.grid.addWidget(self.machinenumber, 2, 2)

        self.label_serialnumber = QLabel('Serial Number')
        self.label_serialnumber.setStyleSheet('''
                            QLabel {
                                text-align: center;
                            }
                        ''')
        self.serialnumber = QLineEdit(self)
        self.serialnumber.setAlignment(Qt.AlignCenter)
        self.serialnumber.setStyleSheet('''
                            QLineEdit {
                                text-align: center;
                                background-color: #1F2843;
                                border: none;
                                border-bottom: 2px solid #1F8EFA;
                            }
                        ''')

        self.grid.addWidget(self.label_serialnumber, 3, 1)
        self.grid.addWidget(self.serialnumber, 3, 2)

        self.btn_confirm = QPushButton(self)
        self.btn_confirm.setText('Confirm')
        self.btn_confirm.setStyleSheet("""
                QPushButton{
                    background-color: #333A51;
                    color: white;
                    border-radius: 10px;
                    padding: 3px 10px 3px 10px;
                    text-align: center;
                    text-decoration: none;
                    margin: 4px 2px;
                    border: 2px solid #6B963B;
                    width: 80px;
                }
                QPushButton:hover {
                    background-color: #5D7C4C;
                }
            """)
        self.btn_confirm.clicked.connect(self.get_license_info)

        self.grid.addWidget(self.btn_confirm, 4, 2)

        self.btn_get_license = QPushButton(self)
        self.btn_get_license.setText('Get License')
        self.btn_get_license.setStyleSheet("""
                        QPushButton{
                            background-color: #333A51;
                            color: white;
                            border-radius: 10px;
                            padding: 3px 10px 3px 10px;
                            text-align: center;
                            text-decoration: none;
                            margin: 4px 2px;
                            border: 2px solid #6B963B;
                            width: 80px;
                        }
                        QPushButton:hover {
                            background-color: #5D7C4C;
                        }
                    """)
        self.btn_get_license.setCursor(Qt.DragLinkCursor)
        self.btn_get_license.clicked.connect(self.redirect_get_license)

        self.grid.addWidget(self.btn_get_license, 4, 1)

        self.machinenumber.setReadOnly(True)
        self.setData()

    def setData(self):
        self.machinenumber.setText(self.value_machinenumber)

    def setData1(self):
        self.serialnumber.setText(self.design.serial_number)

    def redirect_get_license(self):
        webbrowser.open(
            'https://slinkyghxdesign.com/#license')

    def get_date(self, plaintext):
        try:
            time = plaintext[0:4]
            day = plaintext[16:20]
            year = plaintext[32:34]
            return year+day+time
        except Exception as e:
            return '0'

    def get_license_info(self):
        ciphertext = self.serialnumber.text()
        print('ciphertext: ', ciphertext)
        print('current serial: ', self.design.serial_number)
        if ciphertext != self.design.serial_number:
            plaintext = self.caesar_decrypt(ciphertext, 5)

            previous_time = 0
            try:
                previous_time = int(self.get_date(self.caesar_decrypt(self.design.serial_number, 5)))
            except Exception as e:
                previous_time = 0
            current_time = int(self.get_date(plaintext))

            print("previous time", previous_time)
            print("current time", current_time)

            num_design = plaintext[4:8]
            num_analysis = plaintext[20:24]
            design_analysis = num_design + num_analysis

            if current_time > previous_time:
                if plaintext[24:32] + plaintext[8:16] == self.value_machinenumber:
                    if design_analysis == 'g8u4bisk':
                        print('full license')
                        self.design.num_design = '∞'
                        self.design.num_analysis = '∞'
                        self.design.database_set_data()
                        self.design.combobox_selection_changed()
                        self.design.shownotification(resource_path('./Images/success.png'), 'Successfully load!')
                        self.design.serial_number = ciphertext
                    else:
                        try:
                            self.design.num_design += int(num_design)
                            self.design.num_analysis += int(num_analysis)
                            self.design.serial_number = ciphertext
                            self.design.database_set_data()
                            self.design.combobox_selection_changed()
                            self.design.shownotification(resource_path('./Images/success.png'), 'Successfully load!')
                            self.design.serial_number = ciphertext
                        except Exception as e:
                            self.design.shownotification(resource_path("./Image/error.png"), "Invalid license!")

                else:
                    self.design.shownotification(resource_path("./Image/error.png"), "Not this machine!")
            else:
                self.design.shownotification(resource_path('./Images/warning.png'), "Time expired!")
        else:
            self.design.shownotification(resource_path('./Images/warning.png'), "Can't use this number!")

    def caesar_decrypt(self, ciphertext, shift):
        plaintext = ""
        for char in ciphertext:
            # Decrypt uppercase letters
            if char.isupper():
                decrypted_char = chr((ord(char) - 65 - shift) % 26 + 65)
            # Decrypt lowercase letters
            elif char.islower():
                decrypted_char = chr((ord(char) - 97 - shift) % 26 + 97)
            # Decrypt digit
            elif char.isdigit():
                decrypted_char = chr((ord(char) - 48 - shift) % 10 + 48)
            else:
                # Leave non-alphabetic characters unchanged
                decrypted_char = char
            plaintext += decrypted_char
        print("plaintext: ", plaintext)
        return plaintext


class PersonalForm(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet('''
            * {
                background-color: #1F2843;
                color: white;
                font-size: 16px;
                padding: 5px 10px;
            }

            QGroupBox {
                border: 1px solid white;
                border-radius: 30%;
            }
        ''')
        self.grid = QGridLayout(self)

        self.label_title = IntroLabel3('Personal Setting')
        self.label_title.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.label_title, 1, 1)

        self.setdefaultdata = QCheckBox('Set Default Data')
        self.grid.addWidget(self.setdefaultdata, 2, 1)

        self.automateupgrate = QCheckBox('Automate Upgrade')
        self.grid.addWidget(self.automateupgrate, 3, 1)

    def getData(self):
        dict = {
            'Set Default Data': self.setdefaultdata.isChecked(),
            'Automate Upgrade': self.automateupgrate.isChecked()
        }
        return dict

    def setData1(self, data):
        self.setdefaultdata.setChecked(data['Set Default Data'])
        self.automateupgrate.setChecked(data['Automate Upgrade'])


class CustomRadioButton(QRadioButton):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.setIcon(QIcon(image_path))


class CustomRadioButtonGroup(QGroupBox):
    def __init__(self, parent, imagepath):
        super().__init__(parent)

        self.imagepath = imagepath
        self.setStyleSheet('''
            * {
                background-color: #1F2843;
                color: white;
                font-size: 16px;
                padding: 5px 10px;
            }

            QGroupBox {
                border: 1px solid white;
                border-radius: 30%;
            }
        ''')
        self.resize(600, 300)

        self.label_title = IntroLabel3(self)
        self.label_title.setText('Ring Type')
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.move(250, 20)

        self.radiobutton_group = QButtonGroup()

        self.radio_horizontal = QRadioButton(self)
        self.radio_horizontal.setText("Horizontal Slinky")
        self.radio_horizontal.move(100, 100)
        self.radio_horizontal.setChecked(True)
        self.radio_horizontal.clicked.connect(self.radio_horizontal_selection)

        self.radio_vertical = QRadioButton(self)
        self.radio_vertical.setText("Vertical Slinky")
        self.radio_vertical.move(100, 150)
        self.radio_vertical.clicked.connect(self.radio_vertical_selection)

        self.radio_earthbasket = QRadioButton(self)
        self.radio_earthbasket.setText("Earth Basket")
        self.radio_earthbasket.move(100, 200)
        self.radio_earthbasket.clicked.connect(self.radio_earthbasket_selection)

        self.radiobuttons = [self.radio_horizontal, self.radio_vertical, self.radio_earthbasket]

        self.btn_image1 = ImageButton2(self, self.imagepath[0])
        self.btn_image1.move(350, 60)

        self.btn_image2 = ImageButton2(self, self.imagepath[1])
        self.btn_image2.move(350, 60)
        self.btn_image2.hide()

        self.btn_image3 = ImageButton2(self, self.imagepath[2])
        self.btn_image3.move(350, 60)
        self.btn_image3.hide()

        self.btn_images = [self.btn_image1, self.btn_image2, self.btn_image3]

        self.radiobutton_group.addButton(self.radio_horizontal, 0)
        self.radiobutton_group.addButton(self.radio_vertical, 1)
        self.radiobutton_group.addButton(self.radio_earthbasket, 2)

        # print(self.radiobutton_group.checkedId())

    def radio_horizontal_selection(self):
        self.allhide()
        self.btn_image1.show()

    def radio_vertical_selection(self):
        self.allhide()
        self.btn_image2.show()

    def radio_earthbasket_selection(self):
        self.allhide()
        self.btn_image3.show()

    def allhide(self):
        self.btn_image1.hide()
        self.btn_image2.hide()
        self.btn_image3.hide()

    def setData1(self, str):
        num = int(str)
        self.radiobuttons[num].setChecked(True)
        self.allhide()
        self.btn_images[num].show()


class Dialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            background-color: #1F2843;
        """)
        self.setWindowTitle(self.tr("Dialog"))

        # b = ["System Design", ["Inlet Temperature", "dF", "lineedit", '90'],
        #      ["Flow Rate", "gpm/ton", "lineedit", '3.0'], ["Fluid type", ["Water", "Methanol"], "combobox"]]
        # a = InputForm(self, b)

        # c = CustomQTextEdit(self)
        # c.setText("Initial")
        #
        # d = LicenseForm(self)

        e = CustomRadioButtonGroup(self, ['./Images/horizontalslinky.png', './Images/verticalslinky.png',
                                          './Images/earthbasket.png'])

        self.resize(600, 300)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = Dialog()
    w.show()
    sys.exit(app.exec_())
