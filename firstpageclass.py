import sys
import json

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, \
    QAbstractItemView, QHeaderView, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap
from buttonclass import MainButton1
from labelclass import IntroLabel1, IntroLabel3
from notificationclass import CustomMessageBox


class FirstPageClass(QWidget):
    def __init__(self, path, path2, parent=None):
        super().__init__(parent)

        # Set the background color of the main window
        self.setStyleSheet("background-color: #1F2843;")
        self.setFixedSize(910, 790)
        self.parent = parent
        self.path2 = path2

        # Add logo
        label_design = QLabel(self)
        pic_design = QPixmap(path)
        label_design.setPixmap(pic_design.scaled(500, 300))
        label_design.move(250, 50)

        label_design = IntroLabel3(self)
        label_design.setText("Last Design Files")
        label_design.move(100, 400)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setStyleSheet('''
            background-color: #1F2843;
            color: #7C8AA7;
            border: None;
        ''')
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # self.tableWidget.horizontalHeader().setStyleSheet("""
        #     background-color: #2B3651;
        #     color: white;
        # """)
        self.tableWidget.setStyleSheet('''
            font: 'Arial';
            font-size: 16px;
            blockground-color: #1F2843;
            color: #7C8AA7;
            border: none;
        ''')
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.tableWidget.resize(800, 220)
        self.tableWidget.setRowCount(6)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['Path', 'Description'])
        self.tableWidget.move(150, 430)

        btn_open = MainButton1(self)
        btn_open.setText(self.tr('Open Design'))
        btn_open.move(225, 670)
        btn_open.resize(170, 55)
        btn_open.clicked.connect(self.btnopen)

        btn_next = MainButton1(self)
        btn_next.setText(self.tr('Next Step'))
        btn_next.move(575, 670)
        btn_next.resize(170, 55)
        btn_next.clicked.connect(self.btnnext)

    def loadtable(self):
        print('loadtable')
        try:
            with open(self.path2, 'r') as f:
                data = json.load(f)
            print(data)
            for i in range(0, len(data)):
                key = list(data.keys())[len(data) - 1 - i]
                print(key, data[key])
                nameitem = QTableWidgetItem(key)
                nameitem.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(i, 0, nameitem)
                desitem = QTableWidgetItem(data[key])
                desitem.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(i, 1, desitem)
        except Exception as e:
            print('there is not design files')

    def btnopen(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        filepath, _ = QFileDialog.getOpenFileName(self, "Open Design File", "", "GLD Files (*.gld)", options=options)
        if filepath:
            print("filepath", filepath)
            self.parent.currentgldpath = filepath
            self.parent.loaddata()
        else:
            print("no file selected")

    def btnnext(self):
        selected_items = self.tableWidget.selectedItems()
        print('debug btnopen selected item: ', selected_items)
        if len(selected_items) == 2:
            selected_row = selected_items[1].row()
            filepath = self.tableWidget.item(selected_row, 0).text()
            self.parent.currentgldpath = filepath
            self.parent.loaddata()
        else:
            # self.parent.shownotification('./Images/warning.png', 'Select a row.')
            print('btnnext')
            self.parent.movenext()


if __name__ == '__main__':
    # Create a new QApplication instance
    app = QApplication(sys.argv)

    # Create a new MyApp instance
    my_app = FirstPageClass('./Backgrounds/designbackground.png', './Logs/designpath.json')

    # Show the main window
    my_app.show()

    # Start the event loop
    sys.exit(app.exec_())
