import json

# with open('./Logs/designpath.json', 'r') as f:
#     data = json.load(f)
#
# # for i in range(0, len(data)):
# #     for j in range(0, len(data[i])):
# #         print(i, j, data[i][j])
# # print(list(data.keys())[0])
# print(len(data))

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
# import CustomTitleBa

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 500, 500)

        # Create a QTableWidget
        tableWidget = QTableWidget(self)
        tableWidget.setGeometry(50, 50, 400, 400)

        # Set the number of rows and columns in the table
        tableWidget.setRowCount(3)
        tableWidget.setColumnCount(2)

        # Set the column headers
        tableWidget.setHorizontalHeaderLabels(['Name', 'Age'])

        # Add some data to the table
        tableWidget.setItem(0, 0, QTableWidgetItem('John'))
        tableWidget.setItem(0, 1, QTableWidgetItem('30'))
        tableWidget.setItem(1, 0, QTableWidgetItem('Jane'))
        tableWidget.setItem(1, 1, QTableWidgetItem('25'))
        tableWidget.setItem(2, 0, QTableWidgetItem('Bob'))
        tableWidget.setItem(2, 1, QTableWidgetItem('40'))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())