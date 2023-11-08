import json
import sys
import time
import webbrowser
import traceback
import os
import pyperclip

# UI
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QTabWidget, \
    QHBoxLayout, QComboBox, QMessageBox
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import Qt, QSize, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from pyvistaqt import QtInteractor

# Self define
from buttonclass import ImageButton, ExtraButton, SquareButton, ExitButton, MainButton1, ImageButton1, TextButton
from firstpageclass import FirstPageClass
from inputformclass import InputForm, LicenseForm, PersonalForm
from labelclass import IntroLabel1, TickerLabel
from notificationclass import CustomMessageBox, ExitNotification
import pyqtgraph as pg

# Calculation
import numpy as np
from scipy.special import erfc
import math

# license
import hashlib
import uuid
import sqlite3

# 3d model
import pyvista as pv


def resource_path(relative_path):
    return os.path.join(relative_path)


#######################################
########## Design Page ################
#######################################

class EAHEDesignClass(QWidget):
    def __init__(self, parent, path):
        super().__init__(parent)

        ############ System Property ##############
        self.form_openearthtubedesign = None
        self.form_closedearthtubedesign = None
        self.data_form_earthtubedesign = None
        self.form_earthtubedesign = None
        self.systemearthtube = None
        self.systemroomload = None
        self.value_automate_upgrade = None
        self.value_default_data = None
        self.pipeshowframe = None
        self.plotter = None

        self.parent = parent
        self.num_design = 0
        self.num_analysis = 0
        self.program_version = "1.0"
        self.serial_number = ""
        self.value_time_setting = ""
        self.value_personal_setting = {}
        self.value_userinfo = {}

        self.currentpath = os.getcwd()
        self.appdata_dir = path
        self.designpath = self.appdata_dir + '/designpath.json'
        self.init_appdata_dir()

        # Get data
        self.database_connection = sqlite3.connect(self.appdata_dir + "/data.db")

        self.database_cursor = self.database_connection.cursor()
        self.database_get_data()

        self.tabstack = []
        self.dict = {}

        # graph data
        self.tp_series = []
        self.tp_series_0 = []
        self.tp_series_05 = []
        self.tp_series_1 = []
        self.tp_series_2 = []
        self.tp_series_4 = []
        self.t_series = []

        self.image_down_path = resource_path('./Images/down.png')
        print(self.image_down_path)
        self.currentgldpath = ''

        # UI
        self.license_info = None
        self.plt_gfunction = None
        self.radiobutton_group = None

        # calculation
        self.analysis_calculation_result = False
        self.analysis_calculation_process = False

        # set the size of window
        self.setFixedSize(1210, 770)

        # Set the background color of the main window
        self.setStyleSheet("background-color: #1F2843; border: none")

        # add all widgets
        self.left_widget = QWidget()
        self.left_widget.setStyleSheet("""
            background-color: #2C3751;
            border-radius: 10px;
        """)

        # Image button
        self.btn_home = ImageButton(self.left_widget, resource_path('./Images/logo03_glowed_white.png'))
        self.btn_home.move(20, 20)
        self.btn_home.clicked.connect(self.button0)

        self.pipeconductivitytuple = {"Clay": 1, "PEX": 0.14, "Steel": 25, "PVC": 0.41}

        # Remaining Number
        self.combobox_selection = QComboBox(self.left_widget)
        self.icon_design = QIcon(resource_path('./Images/design.png'))
        self.icon_analysis = QIcon(resource_path('./Images/analysis02.png'))
        self.combobox_selection.addItem(self.icon_design, ' Design')
        self.combobox_selection.addItem(self.icon_analysis, 'Analysis ')
        self.combobox_selection.resize(100, 30)
        self.combobox_selection.setCursor(QCursor(Qt.PointingHandCursor))
        self.combobox_selection.setStyleSheet("""            
             QComboBox {
                color: #7C8AA7;
                background-color: #2C3751;
                selection-background-color: white;
                padding: 1px 1px 1px 1px;
                min-width: 2em;
                font-size: 16px;
            }
            
            QComboBox:hover {
                color: #2978FA;
            }
            
            QComboBox::drop-down {
                subcontrol-origin: padding;
                color: white;
                width: 10px;
                border: none;
                padding-right: 3px;
            }
            
            QComboBox QAbstractItemView {
                color: white;
            }
            
            QComboBox::down-arrow {
                border: 0px;
                background-image-width: 30px;
                border-image: url(%s);
            }
        """ % './Images/down.png')
        self.combobox_selection.currentIndexChanged.connect(self.combobox_selection_changed)
        self.combobox_selection.move(20, 155)

        self.label_num = QPushButton(self.left_widget)
        self.label_num_icon = QIcon(resource_path('./Images/remain01.png'))
        self.label_num.setIcon(self.label_num_icon)
        self.label_num.setIconSize(QSize(25, 25))
        self.label_num.setText('' + str(self.num_design))
        self.label_num.setGeometry(130, 155, 75, 30)
        self.label_num.setStyleSheet("""
            QPushButton {
                background-color: #374866;
                color: white;
                font-size: 16px;
                border-radius: 13px;
                transition: background-color 0.9s ease-in-out;
            }
            QPushButton:hover {
                background-color: #5A6B90;
            }
        """)
        self.label_num.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # Left Widget Buttons & Ticker
        self.btn_1 = SquareButton(self.left_widget, resource_path('./Images/configuration01_b.png'),
                                  resource_path('./Images/configuration01.png'))
        self.btn_1.setText(' Room Heat Load ')
        self.btn_1.setGeometry(0, 200, 212, 50)
        self.btn_2 = SquareButton(self.left_widget, resource_path('./Images/fluid02_b.png'),
                                  resource_path('./Images/fluid02.png'))
        self.btn_2.setText(' Earth Tube ')
        self.btn_2.setGeometry(0, 250, 212, 50)

        self.btn_1_ticker = TickerLabel(self.left_widget)
        self.btn_1_ticker.setGeometry(180, 210, 30, 30)
        self.btn_1_ticker.hide()

        self.btn_2_ticker = TickerLabel(self.left_widget)
        self.btn_2_ticker.setGeometry(180, 260, 30, 30)
        self.btn_2_ticker.hide()

        self.btn_3_ticker = TickerLabel(self.left_widget)
        self.btn_3_ticker.setGeometry(180, 310, 30, 30)
        self.btn_3_ticker.hide()

        self.btn_4_ticker = TickerLabel(self.left_widget)
        self.btn_4_ticker.setGeometry(180, 360, 30, 30)
        self.btn_4_ticker.hide()

        self.slide_label = QLabel(self.left_widget)
        self.slide_label.setStyleSheet('background-color: #31A8FC')
        self.slide_label.resize(5, 50)
        self.slide_label.hide()

        self.btn_1.clicked.connect(self.button1)
        self.btn_2.clicked.connect(self.button2)

        # Extra buttons in left widget
        self.btn_setting = ExtraButton(self.left_widget, resource_path('./Images/setting_b.png'),
                                       resource_path('./Images/setting.png'))
        self.btn_setting.setText(' Settings')
        self.btn_setting.setGeometry(0, 590, 200, 50)
        self.btn_setting.clicked.connect(self.btnsetting)

        self.line = QLabel(self.left_widget)
        self.line.setStyleSheet('''
            QLabel {background-color: #ACACBF;;}
        ''')
        self.line.setGeometry(25, 640, 150, 1)

        self.btn_feedback = TextButton(self.left_widget)
        self.btn_feedback.setText(' Feedback')
        self.btn_feedback.clicked.connect(self.redirect_to_feedback)
        self.btn_feedback.setGeometry(50, 650, 100, 20)

        self.btn_help = TextButton(self.left_widget)
        self.btn_help.setText('  Get Manual  ')
        self.btn_help.clicked.connect(self.redirect_to_help)
        self.btn_help.setGeometry(50, 675, 100, 20)

        self.btn_exit = ExitButton(self.left_widget, resource_path('./Images/end01.png'),
                                   resource_path('./Images/end01_r.png'))
        self.btn_exit.setText(' Exit')
        self.btn_exit.setGeometry(0, 695, 200, 50)
        self.btn_exit.clicked.connect(self.btnexit)

        # add tabs
        self.tab1 = self.ui1()
        self.tab2 = self.ui2()
        self.tab3 = self.ui3()
        self.tab9 = self.ui9()

        # right widget
        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")

        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab9, '')

        # self.tab1.loadtable()
        self.right_widget.setCurrentIndex(0)

        self.right_widget.setStyleSheet('''
            QTabWidget::pane {
                border: none;
            }

            QTabBar::tab{
                width: 0;
                height: 0;
                margin: 0;
                padding: 0;
                border: none;
            }
        ''')

        self.setsettings()

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.left_widget)
        main_layout.addWidget(self.right_widget)
        main_layout.setStretch(0, 22)
        main_layout.setStretch(1, 100)
        self.setLayout(main_layout)

    # get project dir
    def init_appdata_dir(self):
        if os.path.isdir(self.appdata_dir):
            print("Folder exists")
        else:
            os.makedirs(self.appdata_dir)
            if os.path.exists(self.designpath):
                print("Design Path exists")
            else:
                with open(self.designpath, 'w') as file:
                    json.dump({self.currentpath + "/Samples/sample.gld": "Design GHE for blockchain mining equipment"},
                              file)
            print("make appdata_dir")

    def check_serial_number(self):
        print("check serial number")

    def database_get_data(self):
        try:
            # get data from db
            self.database_cursor.execute("SELECT * FROM property")
            rows = self.database_cursor.fetchall()
            print("rows: ", rows)

            # set data if data not exist
            if len(rows) > 0:
                json_data = json.loads(rows[-1][1])

                # set class property
                self.num_design = json_data["Design"]
                self.num_analysis = json_data["Analysis"]
                self.program_version = json_data["Program Version"]
                self.serial_number = json_data["Serial Number"]
                self.value_time_setting = json_data["Time Setting"]
                self.value_personal_setting = json_data["Personal Setting"]
                self.value_default_data = self.value_personal_setting["Set Default Data"]
                self.value_automate_upgrade = self.value_personal_setting["Automate Upgrade"]

                print('loaddata')
            elif len(rows) == 0:
                self.database_set_data()

        except Exception as e:
            print('getdata Exception: ', e)
            # create db file if no exist
            self.database_cursor.execute('''CREATE TABLE IF NOT EXISTS property
                              (id INTEGER PRIMARY KEY, data TEXT)''')
            self.database_connection.commit()
            self.database_set_data()

    def database_set_data(self):
        try:
            json_data = {
                'Design': self.num_design,
                'Analysis': self.num_analysis,
                'Program Version': self.program_version,
                'Serial Number': self.serial_number,
                'Time Setting': self.value_time_setting,
                'Personal Setting': self.value_personal_setting
            }

            self.database_cursor.execute("insert into property (data) values (?)", (json.dumps(json_data),))
            self.database_connection.commit()
            print("Completely store data")
            return True
        except Exception as e:
            print('Set data Exception: ', e)
            self.shownotification(resource_path('./Images/error.png'), "Can't Open Database!")
            return False

    def get_machine_number(self):
        # Get operating system version
        mac_address = uuid.getnode()

        # Combine OS version and program version
        combined_str = f"{mac_address}-{self.program_version}"

        # Generate a hash of the combined string
        hash_value = hashlib.md5(combined_str.encode()).hexdigest()
        machine_number = hash_value[:16]
        return machine_number

    def tickerbutton(self):
        print("tickerbutton")

    # combobox
    def combobox_selection_changed(self):
        selected_text = self.combobox_selection.currentText()
        print(selected_text)
        if selected_text == ' Design':
            self.label_num.setText(' ' + str(self.num_design))
        else:
            self.label_num.setText(' ' + str(self.num_analysis))

    # -----------------
    # buttons
    def button0(self):
        print("button0")
        self.right_widget.clear()
        self.tab1 = self.ui1()
        self.tab2 = self.ui2()
        self.tab3 = self.ui3()
        self.tab9 = self.ui9()

        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab9, '')

        self.tab1.loadtable()
        self.right_widget.setCurrentIndex(0)
        self.tickerbutton()
        self.dict = {}
        self.btn_1_ticker.hide()
        self.btn_2_ticker.hide()

    def button0notransition(self):
        print("button0notransition")
        self.right_widget.clear()
        self.tab1 = self.ui1()
        self.tab2 = self.ui2()
        self.tab3 = self.ui3()
        self.tab9 = self.ui9()

        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab9, '')

        self.tab1.loadtable()
        self.right_widget.setCurrentIndex(0)
        self.tickerbutton()
        self.dict = {}
        self.btn_1_ticker.hide()
        self.btn_2_ticker.hide()

    def button1(self):
        self.right_widget.setCurrentIndex(1)
        self.tickerbutton()

    def button2(self):
        self.right_widget.setCurrentIndex(2)
        self.tickerbutton()

    def button7(self):
        # self.right_widget.setCurrentIndex(7)
        if len(self.dict.keys()) == 8:
            self.right_widget.setCurrentIndex(7)
            self.tickerbutton()
        elif len(self.dict.keys()) == 7:
            self.shownotification(resource_path('./Images/warning.png'), "You didn't analyze.")
        else:
            self.shownotification(resource_path('./Images/warning.png'), 'Input all parameters.')

    def btnsetting(self):
        self.right_widget.setCurrentIndex(3)

    def shownotification(self, iconpath, message):
        icon = QIcon(iconpath)
        custom_message_box = CustomMessageBox(icon, 'Custom Message', message, self)
        custom_message_box.setGeometry(950, 20, 300, 70)
        custom_message_box.show()

    def update_pipe(self):
        pipe_data = self.form_pipeproperties.getData()
        outer_diameter = float(list(pipe_data.values())[0])
        inner_diameter = float(list(pipe_data.values())[1])
        print(outer_diameter, inner_diameter)

        outer_cylinder = pv.Cylinder(radius=outer_diameter / 2, height=outer_diameter * 4, resolution=100).triangulate()
        inner_cylinder = pv.Cylinder(radius=inner_diameter / 2, height=outer_diameter * 4, resolution=100).triangulate()

        tube = outer_cylinder - inner_cylinder

        self.plotter = QtInteractor(self.pipeshowframe)
        self.plotter.camera_position = [(0.15, -0.15, 0.15), (0, 0, 0), (0, 0, 0.15)]
        self.plotter.background_color = "#1F2843"
        self.plotter.add_mesh(tube, color='blue')
        self.plotter.setGeometry(50, 30, 700, 230)
        self.plotter.show()

    # -----------------
    # pages

    def ui1(self):
        main = FirstPageClass(resource_path('./Images/designbackground.png'), self.designpath, self)
        main.loadtable()
        return main

    def ui2(self):
        #       Room Load Calculator
        main = QWidget()

        label = IntroLabel1(main)
        label.setText("Room Load Calculator")
        label.move(320, 30)

        self.data_form_fluidproperties = ["Room Load",
                                          ["Material",
                                           ["Concrete",
                                            "Hempcrete",
                                            "Brick",
                                            "Plastic"], "combobox"],
                                          ["External Wall", "m^2", "lineedit", "15"],
                                          ["Roof", "m^2", "lineedit", "20"],
                                          ["Window", "m^2", "lineedit", "7"],
                                          ["Ground Floor", "m^2", "lineedit", "20"],
                                          ["Inner Temp", "⁰C", "lineedit", "18"],
                                          ["Outer Temp", "⁰C", "lineedit", "38"],
                                          ]
        self.form_fluidproperties = InputForm(main, self.data_form_fluidproperties, self)
        self.form_fluidproperties.move(257, 100)

        def calculateroomload():
            if self.num_design > 0:
                try:
                    print("calculate room load")
                    coefficient = {
                        "Concrete": {'External Wall': 0.23, 'Ground Floor':0.3, 'Roof':0.18, 'Window': 0.18},
                        "Hempcrete": {'External Wall': 0.23, 'Ground Floor': 0.3, 'Roof': 0.18, 'Window': 0.18},
                        "Brick": {'External Wall': 0.23, 'Ground Floor': 0.3, 'Roof': 0.18, 'Window': 0.18},
                        "Plastic": {'External Wall': 0.23, 'Ground Floor': 0.3, 'Roof': 0.18, 'Window': 0.18}
                    }
                    dict = self.form_fluidproperties.getData()
                    print('roomload', dict)

                    externalwall = float(dict['External Wall'])
                    groundfloor = float(dict['Ground Floor'])
                    roof = float(dict['Roof'])
                    window = float(dict['Window'])

                    heatloadcoefficient = externalwall*coefficient[dict['Material']]['External Wall'] + groundfloor*coefficient[dict['Material']]['Ground Floor'] + roof*coefficient[dict['Material']]['Roof'] + window*coefficient[dict['Material']]['Window']
                    heatload = heatloadcoefficient * ( float(dict['Outer Temp']) - float(dict['Inner Temp']) )
                    print('heatload', heatload)
                    self.shownotification(resource_path('./Images/success.png'), 'Result: ' + str(heatload) + ' !')
                    pyperclip.copy(str(heatload))
                    self.num_design = self.num_design - 1
                    return heatload
                except Exception as e:
                    self.shownotification(resource_path('./Images/error.png'), "Calculation Error!")
            else:
                self.shownotification(resource_path('./Images/error.png'), "Get license!")

        btn_open = MainButton1(main)
        btn_open.setText(main.tr('Calculate and Copy'))
        btn_open.move(310, 460)
        btn_open.resize(270, 55)
        btn_open.clicked.connect(calculateroomload)
        return main

    def ui3(self):
        # Soil
        main = QTabWidget()
        main.tabBar().setObjectName('mainTab')

        tab1 = self.ui4()
        tab2 = self.ui5()

        main.addTab(tab1, 'Closed Loop')
        main.addTab(tab2, 'Open Loop')

        main.setStyleSheet("""
            QTabWidget::pane {
                background-color: #f2f2f2;
                padding: 0px;
            }
            QTabBar::tab {
                background-color: #2F3B55;
                color: #ffffff;
                font-size: 20px;
                padding: 8px;
                width: 460px;
                height: 30px;
                border-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: #1F2843;
            }

            QTabBar::tab:hover {
                text-decoration: underline;
            }
        """)

        return main

    def ui4(self):
        # Closed loop
        main = QWidget()

        label = IntroLabel1(main)
        label.setText(" Earth Tube Calculator ")
        label.move(320, 30)

        self.data_form_closedearthtubedesign = ["Earth Tube",
                                                ["Heat Load", "W", "lineedit", "200"],
                                                ["Ground Temp", "⁰C", 'lineedit', "15"],
                                                ["Room Temp", "⁰C", 'lineedit', '25'],
                                                ["Pipe Inner Diameter", "m", "lineedit", '0.19'],
                                                ["Pipe Outer Diameter", "m", "lineedit", '0.2'],
                                                ["Pipe Material", ["Clay", "PEX", "PVC", "Steel"], "combobox"],
                                                ["Buried Depth", "m", "lineedit", '2'],
                                                ["Fan Velocity", "m/s", "lineedit", '1.5']
                                                ]
        self.form_closedearthtubedesign = InputForm(main, self.data_form_closedearthtubedesign, self)
        self.form_closedearthtubedesign.move(242, 100)

        btn_open = MainButton1(main)
        btn_open.setText(main.tr('Calculate Earth tube'))
        btn_open.move(320, 530)
        btn_open.resize(300, 55)

        def calculateearthtube():
            self.dict['System'] = self.form_closedearthtubedesign.getData()
            print('closed loop', self.dict['System'])
            self.closedresult()

        btn_open.clicked.connect(calculateearthtube)
        return main

    def ui5(self):
        # Open Loop
        main = QWidget()

        label = IntroLabel1(main)
        label.setText(" Earth Tube Calculator ")
        label.move(320, 30)

        self.data_form_openearthtubedesign = ["Earth Tube",
                                                ["Heat Load", "W", "lineedit", "200"],
                                                ["Ground Temp", "⁰C", 'lineedit', "15"],
                                                ["Room Temp", "⁰C", 'lineedit', '25'],
                                                ["Input Air Temp", "⁰C", 'lineedit', '38'],
                                                ["Pipe Inner Diameter", "m", "lineedit", '0.19'],
                                                ["Pipe Outer Diameter", "m", "lineedit", '0.2'],
                                                ["Pipe Material", ["Clay", "PEX", "PVC", "Steel"], "combobox"],
                                                ["Buried Depth", "m", "lineedit", '2'],
                                                ["Fan Velocity", "m/s", "lineedit", '1.5']
                                                ]
        self.form_openearthtubedesign = InputForm(main, self.data_form_openearthtubedesign, self)
        self.form_openearthtubedesign.move(242, 100)

        btn_open = MainButton1(main)
        btn_open.setText(main.tr('Calculate Earth tube'))
        btn_open.move(320, 530)
        btn_open.resize(300, 55)

        def calculateearthtube():
            self.dict['System'] = self.form_openearthtubedesign.getData()
            print('open loop', self.dict['System'])
            self.openresult()

        btn_open.clicked.connect(calculateearthtube)
        return main

    def ui9(self):
        # Settings
        main = QWidget()

        label = IntroLabel1(main)
        label.setText("Settings")
        label.move(425, 30)

        self.license_info = LicenseForm(main, self)
        self.license_info.resize(600, 200)
        self.license_info.move(200, 100)

        self.data_time_setting = ['Time Setting',
                                  ['Prediction Time', ['10 days', '20 days', '1 month', '2 month', '6 month'],
                                   'combobox']
                                  ]

        self.time_setting = InputForm(main, self.data_time_setting, self)
        self.time_setting.resize(300, 100)
        self.time_setting.move(80, 350)

        self.personal_setting = PersonalForm(main)
        self.personal_setting.resize(300, 137)
        self.personal_setting.move(80, 470)

        web_view = QWebEngineView(main)
        file_path = self.currentpath + "\HTML\About.html"
        web_view.load(QUrl.fromLocalFile(file_path))
        web_view.setAttribute(Qt.WA_StyledBackground)
        web_view.setStyleSheet("""
                            QWebEngineView { 
                                border: 1px solid white;
                                border-radius: 50px;
                                padding: 20px;
                            }
                        """)
        web_view.setContentsMargins(10, 20, 30, 20)
        web_view.setGeometry(405, 350, 460, 260)

        # self.data_userinfo = ['User Info',
        #                       ['Username', '', 'lineedit', '**** ****'],
        #                       ['Gmail', '', 'lineedit', 'default@gmail.com'],
        #                       ['Purpose', '', 'lineedit', 'Residental Building'],
        #                       ['Country', '', 'lineedit', 'Canada'],
        #                       ['Phone', '', 'lineedit', '1010101010']
        #                       ]
        # self.userinfo = InputForm(main, self.data_userinfo)
        # self.userinfo.move(500, 350)

        self.btn_save_settings = QPushButton(main)
        self.btn_save_settings.setText('Save Settings')
        self.btn_save_settings.setStyleSheet("""
                QPushButton{
                    background-color: #333A51;
                    color: white;
                    border-radius: 15px;
                    padding: 3px 10px 3px 10px;
                    text-align: center;
                    text-decoration: none;
                    margin: 4px 2px;
                    border: 2px solid #6B963B;
                    font-size: 16px;
                    height: 30px;
                    width: 140px;
                }
                QPushButton:hover {
                    background-color: #5D7C4C;
                }
            """)
        self.btn_save_settings.move(400, 650)
        self.btn_save_settings.clicked.connect(self.savesettings)
        return main

    def savesettings(self):
        try:
            self.value_time_setting = self.time_setting.getData()
            print(self.value_time_setting)
            self.value_personal_setting = self.personal_setting.getData()
            print(self.value_personal_setting)
            if self.database_set_data():
                self.shownotification(resource_path('./Images/success.png'), 'Save successfully!')
        except Exception as e:
            self.shownotification(resource_path('./Images/error.png'), "Can't Save Settings!")
        try:
            self.database_get_data()
            self.button0notransition()
        except Exception as e:
            self.shownotification(resource_path('./Images/error.png'), "Can't Load Pages!")

    def setsettings(self):
        self.license_info.setData1()
        print(self.value_time_setting, self.value_personal_setting)
        try:
            self.time_setting.setData1(list(self.value_time_setting.values()))
            self.personal_setting.setData1(self.value_personal_setting)
        except Exception as e:
            print("initial setSetting")

    def loaddata(self):
        print("loaddata")
        try:
            with open(self.currentgldpath, 'r') as f:
                context = json.load(f)
                print(context)
        except:
            self.shownotification(resource_path('./Images/warning.png'), "Can't find the file!")
            return False

        if len(context) < 6:
            self.shownotification(resource_path("./Images/error.png"), "This file is corrupted!")
            return False
        else:
            self.form_systemdesign.setData1(list(context['System'].values()))
            self.radiobutton_group.setData1(context['System']['type'])
            self.btn_1_ticker.show()
            self.dict['System'] = context['System']

            self.form_fluidproperties.setData1(list(context['Fluid'].values()))
            self.btn_2_ticker.show()
            self.dict['Fluid'] = context['Fluid']

            self.form_soilthermalproperties.setData1(list(context['Soil'].values()))
            self.btn_3_ticker.show()
            self.dict['Soil'] = context['Soil']

            self.form_pipeproperties.setData1(list(context['Pipe'].values()))
            self.btn_4_ticker.show()
            self.dict['Pipe'] = context['Pipe']

            self.form_circulationpumps.setData1(list(context['Pump'].values()))
            self.btn_5_ticker.show()
            self.dict['Pump'] = context['Pump']

            self.form_designdimensions.setData1(list(context['Results'].values()))
            self.form_designdimensions.setReadOnly(True)
            self.textedit_description.setText(context['Description'])
            self.btn_6_ticker.show()
            self.dict['Results'] = context['Results']
            self.dict['Description'] = context['Description']
            # print(context)

            self.right_widget.setCurrentIndex(6)
            self.shownotification(resource_path('./Images/success.png'), 'Load successfully!')
        return True

    def redirect_to_feedback(self):
        webbrowser.open(
            'https://slinkyghxdesign.com/#contact')

    def redirect_to_help(self):
        webbrowser.open(
            'https://slinkyghxdesign.com/resource')

    def exitbutton(self):
        self.parent.exit()

    def closedsizing(self):
        # System
        try:
            E_heat = float(self.dict['System']['Heat Load'])  # heat load [W]
            print(self.dict['System'])
            T_in = float(self.dict['System']['Room Temp'])  # Hot Fluid Temperature 60~65⁰C, 140~150⁰F

            # Air
            mu = 0.000018
            c_p = 718
            rho = 1.225

            # Soil
            k_soil = 2.07
            T_g = float(self.dict['System']["Ground Temp"])

            # print(E_heat, T_in, mu, c_p, rho, k_soil, T_g)

            # Pipe
            D_i = float(self.dict['System']['Pipe Inner Diameter'])
            D_o = float(self.dict['System']['Pipe Outer Diameter'])
            k_pipe = self.pipeconductivitytuple[self.dict['System']['Pipe Material']]
            d = float(self.dict['System']['Buried Depth'])

            # Pump
            V = float(self.dict['System']["Fan Velocity"])  # modify

        except Exception as e:
            print('Exception: ', traceback.format_exc())
            self.shownotification(resource_path("./Images/warning.png"), "Didn't input all variables.")
            return False
        try:
            # Resistance
            R_e = rho * V * D_i / mu  # Reynolds number    Re<2100 laminar regime; 2100<Re<10000: transitional regime;
            # Re>10000 turbulent regime
            P_r = mu * c_p / k_pipe  # Prandtl number
            h_w = 0.023 * R_e ** 0.8 * P_r ** 0.3 * k_pipe / D_i  # heat transfer coefficient [W/(m^2*k)]

            R_conv = 1 / (3.14159 * D_i * h_w)
            R_pipe = math.log(D_o / D_i) / (2 * 3.14159 * k_pipe)
            S = 2 * 3.14159 / math.log((2 * d / D_o) + math.sqrt((2 * d / D_o) ** 2 - 1))  # conduction shape factor of
            # the pipe
            R_soil = 1 / (S * k_soil)

            R_total = R_conv + R_pipe + R_soil

            # Length calculation
            m_w = rho * V * 3.14159 * (D_i / 2) ** 2
            T_out = T_in - E_heat / (m_w * c_p)
            delta_T = T_in - T_out
            theta_w_in = T_in - T_g
            theta_w_out = T_out - T_g

            print(m_w, c_p, R_total, theta_w_in, theta_w_out)
            L = (m_w * c_p * R_total) * math.log(theta_w_in / theta_w_out)
            L= L * 1.8
            print("length of pipe:", L)
            print("output temperature", T_out)

            dict = {}
            dict['Pipe Length'] = str(L + 2 * d)
            dict['Inlet Temperature'] = str(T_in)
            dict['Outlet Temperature'] = str(delta_T)
            dict['System Flow Rate'] = str(V)
            self.dict['closedResults'] = dict

            if self.num_analysis == '∞':
                print('full license access')
            else:
                self.num_design -= 1
                self.database_set_data()
                self.combobox_selection_changed()
            return True
        except Exception as e:
            print('Size Calculation Error:', traceback.format_exc())
            self.shownotification(resource_path("./Images/error.png"), "Calculation Error!!")
            return False

    def closedresult(self):
        if self.num_analysis > 0:
            self.closedsizing()
        else:
            self.shownotification(resource_path('./Images/error.png'), "Get license!")

    def opensizing(self):
        # System
        try:
            self.closedsizing()
            E_heat = float(self.dict['System']['Heat Load'])  # heat load [W]
            T_in = float(self.dict['System']['Input Air Temp'])  # Hot Fluid Temperature 60~65⁰C, 140~150⁰F
            T_room = float(self.dict['System']['Room Temp'])

            # Air
            mu = 0.000018
            c_p = 718
            rho = 1.225

            # Soil
            k_soil = 2.07
            T_g = float(self.dict['System']["Ground Temp"])

            # print(E_heat, T_in, mu, c_p, rho, k_soil, T_g)

            # Pipe
            D_i = float(self.dict['System']['Pipe Inner Diameter'])
            D_o = float(self.dict['System']['Pipe Outer Diameter'])
            k_pipe = self.pipeconductivitytuple[self.dict['System']['Pipe Material']]
            d = float(self.dict['System']['Buried Depth'])

            # Pump
            V = float(self.dict['System']["Fan Velocity"])  # modify
            E_heat = (T_in - T_room) * c_p * 3.14159 * (D_i/2) * (D_i/2) *V
            print("additional heat", E_heat)

        except Exception as e:
            print('Exception: ', traceback.format_exc())
            self.shownotification(resource_path("./Images/warning.png"), "Didn't input all variables.")
            return False
        try:
            # Resistance
            R_e = rho * V * D_i / mu  # Reynolds number    Re<2100 laminar regime; 2100<Re<10000: transitional regime;
            # Re>10000 turbulent regime
            P_r = mu * c_p / k_pipe  # Prandtl number
            h_w = 0.023 * R_e ** 0.8 * P_r ** 0.3 * k_pipe / D_i  # heat transfer coefficient [W/(m^2*k)]

            R_conv = 1 / (3.14159 * D_i * h_w)
            R_pipe = math.log(D_o / D_i) / (2 * 3.14159 * k_pipe)
            S = 2 * 3.14159 / math.log((2 * d / D_o) + math.sqrt((2 * d / D_o) ** 2 - 1))  # conduction shape factor of
            # the pipe
            R_soil = 1 / (S * k_soil)

            R_total = R_conv + R_pipe + R_soil

            # Length calculation
            m_w = rho * V * 3.14159 * (D_i / 2) ** 2
            T_out = T_in - E_heat / (m_w * c_p)
            delta_T = T_in - T_out
            theta_w_in = T_in - T_g
            theta_w_out = T_out - T_g

            print(m_w, c_p, R_total, theta_w_in, theta_w_out)
            L = (m_w * c_p * R_total) * math.log(theta_w_in / theta_w_out)
            L= L * 1.8
            L = L + float(self.dict['closedResults']['Pipe Length'])
            print("length of pipe:", L)
            print("output temperature", T_out)

            dict = {}
            dict['Pipe Length'] = str(L + 2 * d)
            dict['Inlet Temperature'] = str(T_in)
            dict['Outlet Temperature'] = str(delta_T)
            dict['System Flow Rate'] = str(V)
            self.dict['openResults'] = dict

            if self.num_analysis == '∞':
                print('full license access')
            else:
                self.num_design -= 1
                self.database_set_data()
                self.combobox_selection_changed()
            return True
        except Exception as e:
            print('Size Calculation Error:', traceback.format_exc())
            self.shownotification(resource_path("./Images/error.png"), "Calculation Error!!")
            return False

    def openresult(self):
        if self.num_analysis > 0:
            self.opensizing()
        else:
            self.shownotification(resource_path('./Images/error.png'), "Get license!")

    def btnexit(self):
        self.setEnabled(False)
        notification = ExitNotification(self)
        result = notification.exec_()

        if result == QMessageBox.No:
            self.setEnabled(True)
            return True

        elif result == QMessageBox.Yes:
            sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DesignClass('C:/Users/Bruce/AppData/Roaming/EAHE')
    ex.show()
    sys.exit(app.exec_())
