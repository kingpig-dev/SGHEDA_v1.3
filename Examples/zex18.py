from PyQt5.QtCore import QStandardPaths
import os

appdata_dir = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)

print(os.getcwd())
print(appdata_dir)