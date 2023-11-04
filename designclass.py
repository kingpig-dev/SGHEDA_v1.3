import json
import sys
import threading
import time
import webbrowser
import traceback
import os

# UI
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QTabWidget, \
    QHBoxLayout, QComboBox, QFileDialog, QScrollArea, QMessageBox, QLineEdit, QFrame
from PyQt5.QtGui import QIcon, QCursor, QMovie
from PyQt5.QtCore import Qt, QSize, QTimer, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from pyvistaqt import QtInteractor

# Self define
from buttonclass import ImageButton, ExtraButton, SquareButton, ExitButton, MainButton1, ImageButton1, TextButton
from firstpageclass import FirstPageClass
from inputformclass import InputForm, CustomQTextEdit, LicenseForm, PersonalForm, CustomRadioButtonGroup, \
    Pipe_InputForm, DesignInputForm
from labelclass import IntroLabel1, TickerLabel, IntroLabel3, IntroLabel2
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

class DesignClass(QWidget):
    def __init__(self, parent, path):
        super().__init__(parent)

        ############ System Property ##############
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
        self.btn_1.setText(' System Design ')
        self.btn_1.setGeometry(0, 200, 212, 50)
        self.btn_2 = SquareButton(self.left_widget, resource_path('./Images/fluid02_b.png'),
                                  resource_path('./Images/fluid02.png'))
        self.btn_2.setText(' Fluid Properties ')
        self.btn_2.setGeometry(0, 250, 212, 50)
        self.btn_3 = SquareButton(self.left_widget, resource_path('./Images/soil01_b.png'),
                                  resource_path('./Images/soil01.png'))
        self.btn_3.setText(' Soil Properties ')
        self.btn_3.setGeometry(0, 300, 212, 50)
        self.btn_4 = SquareButton(self.left_widget, resource_path('./Images/pipe01_b.png'),
                                  resource_path('./Images/pipe01.png'))
        self.btn_4.setText(' Pipe Design')
        self.btn_4.setGeometry(0, 350, 212, 50)
        self.btn_5 = SquareButton(self.left_widget, resource_path('./Images/power02_b.png'),
                                  resource_path('./Images/power02.png'))
        self.btn_5.setText(' Pump Info ')
        self.btn_5.setGeometry(0, 400, 212, 50)
        self.btn_6 = SquareButton(self.left_widget, resource_path('./Images/result01_b.png'),
                                  resource_path('./Images/result01.png'))
        self.btn_6.setText(' Design Result')
        self.btn_6.setGeometry(0, 450, 212, 50)
        self.btn_7 = SquareButton(self.left_widget, resource_path('./Images/analysis11_b.png'),
                                  resource_path('./Images/analysis11.png'))
        self.btn_7.setText(' Analysis')
        self.btn_7.setGeometry(0, 500, 212, 50)

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

        self.btn_5_ticker = TickerLabel(self.left_widget)
        self.btn_5_ticker.setGeometry(180, 410, 30, 30)
        self.btn_5_ticker.hide()

        self.btn_6_ticker = TickerLabel(self.left_widget)
        self.btn_6_ticker.setGeometry(180, 460, 30, 30)
        self.btn_6_ticker.hide()

        self.btn_7_ticker = TickerLabel(self.left_widget)
        self.btn_7_ticker.setGeometry(180, 510, 30, 30)
        self.btn_7_ticker.hide()

        self.slide_label = QLabel(self.left_widget)
        self.slide_label.setStyleSheet('background-color: #31A8FC')
        self.slide_label.resize(5, 50)
        self.slide_label.hide()

        self.btn_1.clicked.connect(self.button1)
        self.btn_2.clicked.connect(self.button2)
        self.btn_3.clicked.connect(self.button3)
        self.btn_4.clicked.connect(self.button4)
        self.btn_5.clicked.connect(self.button5)
        self.btn_6.clicked.connect(self.button6)
        self.btn_7.clicked.connect(self.button7)

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
        self.tab4 = self.ui4()
        self.tab5 = self.ui5()
        self.tab6 = self.ui6()
        self.tab7 = self.ui7()
        self.tab8 = self.ui8()
        self.tab9 = self.ui9()

        # right widget
        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")

        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab4, '')
        self.right_widget.addTab(self.tab5, '')
        self.right_widget.addTab(self.tab6, '')
        self.right_widget.addTab(self.tab7, '')
        self.right_widget.addTab(self.tab8, '')
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
        currentIndex = self.right_widget.currentIndex()
        # print('currentIndex: ', currentIndex)
        if self.right_widget.currentIndex() == 0:
            self.slide_label.hide()
        else:
            self.slide_label.move(0, 200 + 50 * (currentIndex - 1))
            self.slide_label.show()

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
        self.tab4 = self.ui4()
        self.tab5 = self.ui5()
        self.tab6 = self.ui6()
        self.tab7 = self.ui7()
        self.tab8 = self.ui8()
        self.tab9 = self.ui9()

        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab4, '')
        self.right_widget.addTab(self.tab5, '')
        self.right_widget.addTab(self.tab6, '')
        self.right_widget.addTab(self.tab7, '')
        self.right_widget.addTab(self.tab8, '')
        self.right_widget.addTab(self.tab9, '')

        self.tab1.loadtable()
        self.right_widget.setCurrentIndex(0)
        self.tickerbutton()
        self.dict = {}
        self.btn_1_ticker.hide()
        self.btn_2_ticker.hide()
        self.btn_3_ticker.hide()
        self.btn_4_ticker.hide()
        self.btn_5_ticker.hide()
        self.btn_6_ticker.hide()
        self.btn_7_ticker.hide()

    def button0notransition(self):
        print("button0notransition")
        self.right_widget.clear()
        self.tab1 = self.ui1()
        self.tab2 = self.ui2()
        self.tab3 = self.ui3()
        self.tab4 = self.ui4()
        self.tab5 = self.ui5()
        self.tab6 = self.ui6()
        self.tab7 = self.ui7()
        self.tab8 = self.ui8()
        self.tab9 = self.ui9()

        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab4, '')
        self.right_widget.addTab(self.tab5, '')
        self.right_widget.addTab(self.tab6, '')
        self.right_widget.addTab(self.tab7, '')
        self.right_widget.addTab(self.tab8, '')
        self.right_widget.addTab(self.tab9, '')

        self.tab1.loadtable()
        self.right_widget.setCurrentIndex(0)
        self.tickerbutton()
        self.dict = {}
        self.btn_1_ticker.hide()
        self.btn_2_ticker.hide()
        self.btn_3_ticker.hide()
        self.btn_4_ticker.hide()
        self.btn_5_ticker.hide()
        self.btn_6_ticker.hide()
        self.btn_7_ticker.hide()

    def button1(self):
        self.right_widget.setCurrentIndex(1)
        self.tickerbutton()

    def button2(self):
        self.right_widget.setCurrentIndex(2)
        self.tickerbutton()

    def button3(self):
        self.right_widget.setCurrentIndex(3)
        self.tickerbutton()

    def button4(self):
        self.right_widget.setCurrentIndex(4)
        self.tickerbutton()

    def button5(self):
        self.right_widget.setCurrentIndex(5)
        self.tickerbutton()

    def button6(self):
        self.right_widget.setCurrentIndex(6)
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
        self.right_widget.setCurrentIndex(8)

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
        #         System
        main = QWidget()
        label = IntroLabel1(main)
        label.setText("System")
        label.move(440, 30)

        self.data_form_systemdesign = ["System Design",
                                       ["Heat Load", "W", "lineedit", "2800"],
                                       ["Input Fluid Temperature", "⁰C", "lineedit", '40']]
        self.form_systemdesign = InputForm(main, self.data_form_systemdesign, self)
        self.form_systemdesign.move(257, 100)

        self.radiobutton_group = CustomRadioButtonGroup(main, [resource_path('./Images/horizontalslinky.png'),
                                                               resource_path('./Images/verticalslinky.png'),
                                                               resource_path('./Images/earthbasket.png')])
        self.radiobutton_group.move(180, 300)

        def uimovenext():
            print("uimovenext")
            dict = {}
            if self.form_systemdesign.getValidation():
                dict = self.form_systemdesign.getData()
                dict['type'] = self.radiobutton_group.radiobutton_group.checkedId()
            else:
                self.btn_1_ticker.hide()
                self.movenext()
                return False
            self.btn_1_ticker.show()
            self.dict["System"] = dict
            self.movenext()
            return True

        def uimoveprevious():
            self.moveprevious()

        def setData(data):
            self.form_systemdesign.setData(data['System'])

        btn_open = MainButton1(main)
        btn_open.setText(main.tr('Previous Step'))
        btn_open.move(225, 670)
        btn_open.resize(170, 55)
        btn_open.clicked.connect(uimoveprevious)

        btn_next = MainButton1(main)
        btn_next.setText(main.tr('Next Step'))
        btn_next.move(575, 670)
        btn_next.resize(170, 55)
        btn_next.clicked.connect(uimovenext)
        return main

    def ui3(self):
        #       Fluid
        main = QWidget()

        label = IntroLabel1(main)
        label.setText("Fluid")
        label.move(440, 30)

        self.data_form_fluidproperties = ["Fuild Properties",
                                          ["Fluid Type",
                                           ["Water", "Methanol", "Ethylene Glycol", "Propylene Glycol",
                                            "Sodium Chloride",
                                            "Calcium Chloride"], "combobox"],
                                          ["Viscosity", "Pa*s", "lineedit", "0.001"],
                                          ["Specific Heat", "J/(Kg*⁰C)", "lineedit", "4162"],
                                          ["Density", "Kg/m^3", "lineedit", "1001"]
                                          ]
        self.form_fluidproperties = InputForm(main, self.data_form_fluidproperties, self)
        self.form_fluidproperties.move(257, 100)

        web_view = QWebEngineView(main)
        file_path = self.currentpath + "\HTML\FluidTable.html"
        web_view.load(QUrl.fromLocalFile(file_path))
        web_view.setAttribute(Qt.WA_StyledBackground)
        web_view.setStyleSheet("""
            QWebEngineView { 
                border: 1px solid white;
                border-radius: 50px;
                padding: 50px;
            }
            
            QScrollBar:vertical {
                background-color: #F5F5F5;
                width: 20px;
                margin: 0px;
            }
        
            QScrollBar::handle:vertical {
                background-color: #CCCCCC;
                min-height: 20px;
            }
        
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                background: none;
            }
        """)
        web_view.setContentsMargins(30, 20, 30, 20)
        web_view.setGeometry(100, 350, 800, 300)

        def uimovenext():
            print("uimovenext")
            dict = {}
            if self.form_fluidproperties.getValidation():
                dict = self.form_fluidproperties.getData()
            else:
                self.btn_2_ticker.hide()
                self.movenext()
                return False

            self.dict["Fluid"] = dict
            self.btn_2_ticker.show()
            self.movenext()
            return True

        def uimoveprevious():
            self.moveprevious()

        btn_open = MainButton1(main)
        btn_open.setText(main.tr('Previous Step'))
        btn_open.move(225, 670)
        btn_open.resize(170, 55)
        btn_open.clicked.connect(uimoveprevious)

        btn_next = MainButton1(main)
        btn_next.setText(main.tr('Next Step'))
        btn_next.move(575, 670)
        btn_next.resize(170, 55)
        btn_next.clicked.connect(uimovenext)
        return main

    def ui4(self):
        # Soil
        main = QWidget()

        label = IntroLabel1(main)
        label.setText(" Soil ")
        label.move(440, 30)

        self.data_form_soilthermalproperties = ["Soil Thermal Properties",
                                                ["Thermal Conductivity", "W/(m*K)", "lineedit", "2.07"],
                                                ["Thermal Diffusivity", "m^2/h", 'lineedit', "0.0000001"],
                                                ["Ground Temperature", "⁰C", "lineedit", '20']
                                                ]
        self.form_soilthermalproperties = InputForm(main, self.data_form_soilthermalproperties, self)
        self.form_soilthermalproperties.move(232, 100)

        web_view = QWebEngineView(main)
        file_path = self.currentpath + "\HTML\SoilTable.html"
        web_view.load(QUrl.fromLocalFile(file_path))
        web_view.setAttribute(Qt.WA_StyledBackground)
        web_view.setStyleSheet("""
                    QWebEngineView { 
                        border: 1px solid white;
                        border-radius: 50px;
                        padding: 50px;
                    }
                """)
        web_view.setContentsMargins(30, 20, 30, 20)
        web_view.setGeometry(100, 300, 800, 350)

        def uimovenext():
            print("uimovenext")
            dict = {}
            if self.form_soilthermalproperties.getValidation():
                dict = self.form_soilthermalproperties.getData()
            else:
                self.btn_3_ticker.hide()
                self.movenext()
                return False

            self.dict["Soil"] = dict
            self.btn_3_ticker.show()
            self.movenext()
            return True

        def uimoveprevious():
            self.moveprevious()

        btn_open = MainButton1(main)
        btn_open.setText(main.tr('Previous Step'))
        btn_open.move(225, 670)
        btn_open.resize(170, 55)
        btn_open.clicked.connect(uimoveprevious)

        btn_next = MainButton1(main)
        btn_next.setText(main.tr('Next Step'))
        btn_next.move(575, 670)
        btn_next.resize(170, 55)
        btn_next.clicked.connect(uimovenext)

        return main

    def ui5(self):
        # Pipe
        main = QWidget()

        label = IntroLabel1(main)
        label.setText(" Pipe")
        label.move(440, 30)

        # self.data_form_pipeproperties = ["Pipe Properties",
        #                                  ["Pipe Size",
        #                                   ["3/4 in. (21mm)", "1 in. (25mm)", "1 1/4 in. (32mm)", "1 1/2 in. (40mm)"],
        #                                   "combobox"],
        #                                  ["Outer Diameter", "m", "lineedit", '0.021'],
        #                                  ["Inner Diameter", "m", "lineedit", '0.026'],
        #                                  ["Pipe Conductivity", "W/(m*K)", "lineedit", '0.14']
        #                                  ]
        self.data_form_pipeproperties = ["Pipe Properties",
                                         ["Outer Diameter", "m", "lineedit", '0.026'],
                                         ["Inner Diameter", "m", "lineedit", '0.021'],
                                         ["Pipe Conductivity", "W/(m*K)", "lineedit", '0.14'],
                                         ['Buried Depth', 'm', 'lineedit', '2.0']
                                         ]
        self.form_pipeproperties = InputForm(main, self.data_form_pipeproperties, self)
        self.form_pipeproperties.move(257, 100)

        # self.data_form_pipeconfiguration = ["Pipe Configuration",
        #                                     ["Pipe Conductivity", "W/(m*K)", "lineedit", '0.14']]
        # self.form_pipeconfiguration = InputForm(main, self.data_form_pipeconfiguration)
        # self.form_pipeconfiguration.move(287, 450)

        inner_diameter = 0.021
        outer_diameter = 0.026
        height = outer_diameter * 4

        # Create the outer cylinder
        outer_cylinder = pv.Cylinder(radius=outer_diameter / 2, height=height, resolution=128).triangulate()

        # Create the inner cylinder
        inner_cylinder = pv.Cylinder(radius=inner_diameter / 2, height=height+0.2, resolution=128).triangulate()

        # Create the tube by subtracting the inner cylinder from the outer cylinder
        tube = outer_cylinder - inner_cylinder

        self.pipeshowframe = QFrame(main)
        self.pipeshowframe.setStyleSheet("""
             QFrame {
             border: 1px solid white;
             border-radius: 30%;
             }
        """)
        self.pipeshowframe.setGeometry(100, 350, 800, 300)

        self.plotter = QtInteractor(self.pipeshowframe)
        self.plotter.camera_position = [(0.15, -0.15, 0.15), (0, 0, 0), (0, 0, 0.15)]
        self.plotter.background_color = "#1F2843"
        self.plotter.add_mesh(tube, color='blue')
        self.plotter.setGeometry(50, 30, 700, 230)
        self.plotter.show()

        iconpath = self.currentpath + "/Images/refresh.png"
        refresh_button = QPushButton(self.pipeshowframe)
        refresh_button.setIcon(QIcon(iconpath))
        refresh_button.setToolTip('refresh')
        refresh_button.setIconSize(QSize(25, 25))
        refresh_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        refresh_button.clicked.connect(self.update_pipe)
        refresh_button.setGeometry(0, 0, 25, 25)

        def uimovenext():
            print("uimovenext")
            dict = {}
            if self.form_pipeproperties.getValidation():
                dict = self.form_pipeproperties.getData()
            else:
                self.btn_4_ticker.hide()
                self.movenext()
                return False

            self.dict["Pipe"] = dict
            self.btn_4_ticker.show()
            self.movenext()
            return True

        def uimoveprevious():
            self.moveprevious()

        btn_open = MainButton1(main)
        btn_open.setText(main.tr('Previous Step'))
        btn_open.move(225, 670)
        btn_open.resize(170, 55)
        btn_open.clicked.connect(uimoveprevious)

        btn_next = MainButton1(main)
        btn_next.setText(main.tr('Next Step'))
        btn_next.move(575, 670)
        btn_next.resize(170, 55)
        btn_next.clicked.connect(uimovenext)

        return main

    def ui6(self):
        # Pump
        main = QWidget()

        label = IntroLabel1(main)
        label.setText("  Pump")
        label.move(440, 30)

        self.data_form_circulationpumps = ["Circulation Pump",
                                           ["Required Power", 'W', "lineedit", '600'],
                                           ["Fluid Velocity", "m/s", 'lineedit', '1.5'],
                                           ['Pump Motor Efficiency', '%', 'lineedit', '85']
                                           ]
        self.form_circulationpumps = InputForm(main, self.data_form_circulationpumps, self)
        self.form_circulationpumps.move(267, 100)

        web_view = QWebEngineView(main)
        file_path = self.currentpath + "\HTML\PumpTable.html"
        web_view.load(QUrl.fromLocalFile(file_path))
        web_view.setAttribute(Qt.WA_StyledBackground)
        web_view.setStyleSheet("""
                            QWebEngineView { 
                                border: 1px solid white;
                                border-radius: 50px;
                                padding: 50px;
                            }
                        """)
        web_view.setContentsMargins(30, 20, 30, 20)
        web_view.setGeometry(100, 300, 800, 350)

        def end_loading():

            self.left_widget.setEnabled(True)
            loading_label.setVisible(False)
            btn_loading_stop.setVisible(False)
            movie.stop()
            timer.stop()
            self.result()

        # timer object
        timer = QTimer()
        timer.timeout.connect(end_loading)

        def uimoveprevious():
            self.moveprevious()

        def start_loading():
            print("Design")
            if self.num_design == '∞' or self.num_design > 0:
                dict = {}
                if self.form_circulationpumps.getValidation():
                    dict = self.form_circulationpumps.getData()
                else:
                    self.shownotification(resource_path('./Images/warning.png'), "Input all parameters.")
                    return False
                self.dict["Pump"] = dict
                self.btn_5_ticker.show()

                if len(self.dict.keys()) < 5:
                    print('Design1', len(self.dict.keys()))
                    self.shownotification(resource_path('./Images/warning.png'), "Input all parameters.")
                    return False

                loading_label.setVisible(True)
                self.left_widget.setEnabled(False)
                btn_loading_stop.setVisible(True)
                movie.start()
                timer.start(2000)
            else:
                self.shownotification(resource_path('./Images/error.png'), "Get license!")

        def loading_stop():
            self.left_widget.setEnabled(True)
            loading_label.setVisible(False)
            btn_loading_stop.setVisible(False)
            movie.stop()
            timer.stop()

        btn_open = MainButton1(main)
        btn_open.setText(main.tr('Previous Step'))
        btn_open.move(225, 670)
        btn_open.resize(170, 55)
        btn_open.clicked.connect(uimoveprevious)

        btn_next = MainButton1(main)
        btn_next.setText(main.tr('Design'))
        btn_next.move(575, 670)
        btn_next.resize(170, 55)
        btn_next.clicked.connect(start_loading)

        movie = QMovie(resource_path('./Images/loading.gif'))
        loading_label = QLabel(main)
        loading_label.setAlignment(Qt.AlignCenter)
        loading_label.setFixedSize(950, 730)
        loading_label.setVisible(False)
        loading_label.setMovie(movie)
        loading_label.move(20, 0)

        btn_loading_stop = ImageButton1(main, resource_path('./Images/x02.png'))
        btn_loading_stop.setToolTip('Cancel Calculation')
        btn_loading_stop.move(900, 30)
        btn_loading_stop.clicked.connect(loading_stop)
        btn_loading_stop.setVisible(False)

        return main

    def ui7(self):
        # Result
        main = QWidget()

        label = IntroLabel1(main)
        label.setText(" Result")
        label.move(440, 30)

        main.setStyleSheet('''
            * {
                color: white;
            }
            QLineEdit {
                border: 1px solid #767A7D;
            }
            
            QCombobox {
                border: 1px solid #767A7D;
            }
        ''')

        self.data_form_designdimensions = ["Design Dimensions",
                                           ["Ring Diameter", 'm', "lineedit", '0.75'],
                                           ["Pitch", 'm', "lineedit", '0.4'],
                                           ["Number of Ring", '', 'lineedit', '8'],
                                           ["Pipe Length", 'm', "lineedit", '25.6'],
                                           ['Inlet Temperature', '⁰C', 'lineedit', '40'],
                                           ['Diff Temperature', '⁰C', 'lineedit', '3'],
                                           ['System Flow Rate', 'm/s', 'lineedit', '1.5']
                                           ]
        self.form_designdimensions = DesignInputForm(main, self.data_form_designdimensions, self)
        self.form_designdimensions.move(277, 100)

        label_description = IntroLabel3(main)
        label_description.setText('Description')
        label_description.setAlignment(Qt.AlignCenter)
        label_description.move(440, 450)

        self.textedit_description = CustomQTextEdit(main)
        self.textedit_description.setPlaceholderText('Design GHE for blockchain mining equipment')
        self.textedit_description.setGeometry(150, 485, 700, 150)

        def uisavedesign():
            if self.textedit_description.toPlainText() == "":
                self.textedit_description.setText('Design GHE for blockchain mining equipment')
            description = self.textedit_description.toPlainText()
            self.dict["Description"] = description

            if len(self.dict.keys()) >= 7:
                options = QFileDialog.Options()
                options |= QFileDialog.DontUseNativeDialog

                file_path, _ = QFileDialog.getSaveFileName(main, "Save File", "", "Text Files *.gld;;",
                                                           options=options)

                print(file_path)
                if file_path:
                    temp_file_path = file_path.split('/')[-1].split('.')
                    if len(temp_file_path) == 1:
                        file_path = file_path + '.gld'
                    with open(file_path, 'w') as file:
                        file.write(json.dumps(self.dict))
                    with open(self.designpath, 'r') as tablefile:
                        try:
                            tablecontent = json.load(tablefile)
                        except Exception as e:
                            tablecontent = {}
                            print("Design file is empty!")
                    with open(self.designpath, 'w') as savefile:
                        tablecontent[file_path] = description
                        savefile.write(json.dumps(tablecontent))
                return True
            else:
                self.shownotification(resource_path('./Images/warning.png'), "Input all parameters.")
                return False

        def gotoanalysis():
            self.analysis_calculation_result = True
            if self.analysis():
                end_loading()
                self.right_widget.setCurrentIndex(7)
                self.tickerbutton()
                self.btn_7_ticker.show()
                return True
            else:
                return False

        def end_loading():
            self.analysis_calculation_process = False
            self.left_widget.setEnabled(True)
            loading_label.setVisible(False)
            btn_loading_stop.setVisible(False)
            movie.stop()
            self.right_widget.setCurrentIndex(6)

        def start_loading():
            print("start loading")
            self.analysis_calculation_process = True
            loading_label.setVisible(True)
            self.left_widget.setEnabled(False)
            btn_loading_stop.setVisible(True)
            movie.start()
            self.tickerbutton()

        def start_analysis():
            if self.num_analysis == '∞' or self.num_analysis > 0:
                if self.textedit_description.toPlainText() == "":
                    self.textedit_description.setText('Design GHE for blockchain mining equipment')
                description = self.textedit_description.toPlainText()
                self.dict["Description"] = description
                if len(self.dict.keys()) == 7 or len(self.dict.keys()) == 8:
                    start_loading()
                    thread = threading.Thread(target=gotoanalysis)
                    thread.start()

                    # database update
                    if self.num_analysis == "∞":
                        print('full license access')
                    else:
                        self.num_analysis -= 1
                        self.database_set_data()
                        self.combobox_selection_changed()

                else:
                    print(self.dict)
                    self.shownotification(resource_path('./Images/warning.png'), 'Input all parameters.')
            else:
                self.shownotification(resource_path('./Images/error.png'), 'Get license!')

        btn_save = MainButton1(main)
        btn_save.setText(main.tr('Save design'))
        btn_save.move(150, 670)
        btn_save.resize(170, 55)
        btn_save.clicked.connect(uisavedesign)

        btn_redesign = MainButton1(main)
        btn_redesign.setText(main.tr('Redesign'))
        btn_redesign.move(412, 670)
        btn_redesign.resize(170, 55)
        btn_redesign.clicked.connect(self.button0)

        btn_gotoanalysis = MainButton1(main)
        btn_gotoanalysis.setText(main.tr('Go to Analysis'))
        btn_gotoanalysis.move(675, 670)
        btn_gotoanalysis.resize(170, 55)
        btn_gotoanalysis.clicked.connect(start_analysis)

        movie = QMovie(resource_path('./Images/loading.gif'))
        loading_label = QLabel(main)
        loading_label.setAlignment(Qt.AlignCenter)
        loading_label.setFixedSize(730, 730)
        loading_label.setVisible(False)
        loading_label.setMovie(movie)
        loading_label.move(120, 0)

        btn_loading_stop = ImageButton1(main, resource_path('./Images/x02.png'))
        btn_loading_stop.setToolTip('Cancel Calculation')
        btn_loading_stop.move(900, 30)
        btn_loading_stop.clicked.connect(end_loading)
        btn_loading_stop.setVisible(False)

        return main

    def ui8(self):
        # Analysis
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        # scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        label = IntroLabel1(scroll_area)
        label.setText("Analysis")
        label.move(440, 30)

        self.analysis_elapsed_time = IntroLabel2(scroll_area)
        self.analysis_elapsed_time.setText("Elapsed time: ")
        self.analysis_elapsed_time.move(650, 40)

        self.plt_gfunction = pg.PlotWidget(scroll_area)
        self.plt_gfunction.setTitle("G-function")
        self.plt_gfunction.setLabel('left', 'g-function')
        self.plt_gfunction.setLabel('bottom', 'Time(day)')
        self.plt_gfunction.setBackground('#2C3751')
        self.plt_gfunction.setGeometry(150, 80, 700, 290)

        self.plt_temperaturepertubation = pg.PlotWidget(scroll_area)
        self.plt_temperaturepertubation.setTitle('Temperature Pertubation')
        self.plt_temperaturepertubation.setLabel('left', 'degree')
        self.plt_temperaturepertubation.setLabel('bottom', 'Time(day)')
        self.plt_temperaturepertubation.setBackground('#2C3751')
        self.plt_temperaturepertubation.setGeometry(150, 380, 700, 290)

        btn_redesign = MainButton1(scroll_area)
        btn_redesign.setText('Redesign')
        btn_redesign.move(410, 690)
        btn_redesign.resize(170, 55)
        btn_redesign.clicked.connect(self.button0)

        return scroll_area

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

    def movenext(self):
        self.right_widget.setCurrentIndex(self.right_widget.currentIndex() + 1)
        self.tickerbutton()

    def moveprevious(self):
        self.right_widget.setCurrentIndex(self.right_widget.currentIndex() - 1)
        self.tickerbutton()

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

    def sizing(self):
        # System
        try:
            E_heat = float(self.dict['System']['Heat Load'])  # heat load [W]
            T_in = float(self.dict['System']['Input Fluid Temperature'])  # Hot Fluid Temperature 60~65⁰C, 140~150⁰F

            # Fluid
            mu = float(self.dict["Fluid"]["Viscosity"])
            c_p = float(self.dict["Fluid"]["Specific Heat"])
            rho = float(self.dict["Fluid"]["Density"])

            # Soil
            k_soil = float(self.dict["Soil"]["Thermal Conductivity"])
            T_g = float(self.dict["Soil"]["Ground Temperature"])

            # print(E_heat, T_in, mu, c_p, rho, k_soil, T_g)

            # Pipe
            D_i = float(self.dict['Pipe']['Inner Diameter'])
            D_o = float(self.dict['Pipe']['Outer Diameter'])
            k_pipe = float(self.dict['Pipe']['Pipe Conductivity'])
            d = float(self.dict['Pipe']['Buried Depth'])

            # Pump
            V = float(self.dict["Pump"]["Fluid Velocity"])  # modify
            p = float(self.dict['Pump']['Required Power'])

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
            L = L * 1.6
            print("length of pipe:", L)
            ring_diameter = 0.75 * T_in / T_out
            pitch = 0.4 * T_in / T_out

            if self.dict['System']['type'] == 1:
                L = L * 0.95
            elif self.dict['System']['type'] == 2:
                L = L * 0.75
                ring_diameter = ring_diameter * 0.9
                pitch = ring_diameter * 0.92

            dict = {}
            dict['Ring Diameter'] = str(ring_diameter)
            dict['Pitch'] = str(pitch)
            dict['Number of Ring'] = str(L / math.hypot(3.14 * ring_diameter, pitch))
            dict['Pipe Length'] = str(L + 2 * d)
            dict['Inlet Temperature'] = str(T_in)
            dict['Outlet Temperature'] = str(delta_T)
            dict['System Flow Rate'] = str(V)
            self.dict['Results'] = dict

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

    def result(self):
        if self.sizing():
            self.form_designdimensions.setData1(list(self.dict["Results"].values()))
            self.form_designdimensions.setReadOnly(True)
            self.right_widget.setCurrentIndex(6)
            self.tickerbutton()
            self.btn_6_ticker.show()
        else:
            self.tickerbutton()
            print('Show Notification')

    def analysis(self):
        self.tp_series = []
        self.tp_series_0 = []
        self.tp_series_05 = []
        self.tp_series_1 = []
        self.tp_series_2 = []
        self.tp_series_4 = []
        self.t_series = []

        print('Analysis')
        N_ring = round(float(self.dict["Results"]['Number of Ring']) / 10)
        R = float(self.dict["Results"]['Ring Diameter'])  # m
        pitch = float(self.dict['Results']['Pitch'])  # m

        # alpha = 1e-6  # m2/s

        end_time = 0
        if self.value_time_setting["Prediction Time"] == '10 days':
            end_time = 1
        elif self.value_time_setting["Prediction Time"] == '20 days':
            end_time = 2
        elif self.value_time_setting["Prediction Time"] == '1 month':
            end_time = 3
        elif self.value_time_setting["Prediction Time"] == '2 month':
            end_time = 6
        elif self.value_time_setting["Prediction Time"] == '6 month':
            end_time = 18

        print("end time: ", end_time)
        self.t_series = np.arange(0.01, end_time, 0.05)  # consider alpha
        h = float(self.dict['Pipe']['Buried Depth'])  # m

        def sqrt_float16(x):
            return np.sqrt(x).astype(np.float16)

        def erfc_float16(x):
            return erfc(x).astype(np.float16)

        def cos_float16(x):
            return np.cos(x).astype(np.float16)

        def sin_float16(x):
            return np.sin(x).astype(np.float16)

        def quadself(f, a, b, c, d, nx, ny):
            # Function to approximate the double integral
            dx: np.float16 = (b - a) / nx
            dy: np.float16 = (d - c) / ny

            integral_sum: np.float16 = 0.0

            for i in range(nx):
                x = a + (i + 0.5) * dx

                for j in range(ny):
                    y = c + (j + 0.5) * dy
                    integral_sum += f(x, y)

            integral_sum *= dx * dy

            return integral_sum

        start_time = time.time()

        # gs_series = []
        # for N_ring in N_ring_series:
        try:
            gs_series = []
            for t in self.t_series:
                gs = 0
                for i in range(1, N_ring + 1):
                    for j in range(1, N_ring + 1):
                        if self.analysis_calculation_process:
                            if i != j:
                                def d(w: np.float16, phi: np.float16):
                                    return sqrt_float16(
                                        (pitch * (i - j) + R * (cos_float16(phi) - cos_float16(w))) ** 2 +
                                        (R * (sin_float16(phi) - sin_float16(w))) ** 2)

                                def fun(w: np.float16, phi: np.float16):
                                    return erfc_float16(d(w, phi) / (2 * sqrt_float16(t))) / d(w, phi) - erfc_float16(
                                        sqrt_float16(d(w, phi) ** 2 + 4 * h ** 2) / (
                                                2 * sqrt_float16(t))) / sqrt_float16(
                                        d(w, phi) ** 2 + 4 * h ** 2)

                                # b, _ = dblquad(fun, 0, 2 * np.pi, lambda phi: 0, lambda phi: 2 * np.pi,
                                # epsabs=1e-2, epsrel=1e-2)
                                b = quadself(fun, 0, 2 * np.pi, 0, 2 * np.pi, 20, 20)
                                gs += np.float16(b)
                        else:
                            return False
                print(f"gs: {gs}")
                gs_series.append(gs / N_ring)

            self.plt_gfunction.clear()
            self.plt_gfunction.plot(self.t_series * 11.57, gs_series, pen='b')  # 1e6/(3600*24)=11.57

            conductivity = float(self.dict['Soil']['Thermal Conductivity'])
            heatload = float(self.dict['System']['Heat Load']) / pitch

            for a in gs_series:
                self.tp_series.append(-a * heatload / (2 * np.pi * conductivity * 1e5) * 3)
            for i in range(0, len(self.tp_series)):
                self.tp_series_0.append(self.tp_series[i] * erfc(0.01 / np.sqrt(self.t_series[i])))
                self.tp_series_05.append(self.tp_series[i] * erfc(0.5 / np.sqrt(self.t_series[i])))
                self.tp_series_1.append(self.tp_series[i] * erfc(1 / np.sqrt(self.t_series[i])))
                self.tp_series_2.append(self.tp_series[i] * erfc(2 / np.sqrt(self.t_series[i])))
                self.tp_series_4.append(self.tp_series[i] * erfc(4 / np.sqrt(self.t_series[i])))

            self.show_analysis_graph()

            end_time = time.time()
            elapsed_time = end_time - start_time
            print("Elapsed time: {:.2f}".format(elapsed_time))
            self.dict["Analysis"] = {"Elapsed time": str(elapsed_time)}
            self.analysis_elapsed_time.setText("Elapsed time: {:.2f}s".format(elapsed_time))
            return True
        except Exception as e:
            print("analysis calculation error: ", e)
            self.shownotification(resource_path("./Image/error.png"), "Can't calculate analysis")
            return False

    def show_analysis_graph(self):
        self.plt_temperaturepertubation.clear()
        plot_item = self.plt_temperaturepertubation.getPlotItem()

        curve0 = plot_item.plot(self.t_series * 11.57, self.tp_series_0, pen='b', name='0.01m')
        curve1 = plot_item.plot(self.t_series * 11.57, self.tp_series_05, pen='r', name='0.5m')
        curve2 = plot_item.plot(self.t_series * 11.57, self.tp_series_1, pen='w', name='1m')
        curve3 = plot_item.plot(self.t_series * 11.57, self.tp_series_2, pen='y', name='2m')
        curve4 = plot_item.plot(self.t_series * 11.57, self.tp_series_4, pen='g', name='4m')

        legend = pg.LegendItem()
        legend.setParentItem(plot_item)

        legend.addItem(curve0, '0.01m')
        legend.addItem(curve1, '0.5m')
        legend.addItem(curve2, '1m')
        legend.addItem(curve3, '2m')
        legend.addItem(curve4, '4m')
        legend.anchor((0, 0), (0.2, 0.95))

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
    ex = DesignClass()
    ex.show()
    sys.exit(app.exec_())
