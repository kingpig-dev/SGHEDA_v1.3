import sys

# Setting the Qt bindings for QtPy
import os

os.environ["QT_API"] = "pyqt5"

from qtpy import QtWidgets
from qtpy.QtWidgets import QMainWindow

import numpy as np

import pyvista as pv
from pyvistaqt import QtInteractor

import pandas as pd


class MainWindow(QMainWindow):

    def __init__(self, parent=None, show=True):
        QtWidgets.QMainWindow.__init__(self, parent)

        # create the frame
        self.frame = QtWidgets.QFrame()
        vlayout = QtWidgets.QVBoxLayout()

        # add the pyvista interactor object
        self.plotter = QtInteractor(self.frame)
        vlayout.addWidget(self.plotter.interactor)

        self.frame.setLayout(vlayout)
        self.setCentralWidget(self.frame)

        # simple menu to demo functions
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        exitButton = QtWidgets.QAction('Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        # allow adding a sphere
        meshMenu = mainMenu.addMenu('Mesh')
        self.add_sphere_action = QtWidgets.QAction('Add Sphere', self)
        self.add_sphere_action.triggered.connect(self.add_sphere)
        meshMenu.addAction(self.add_sphere_action)

        x = np.array([9, 8, 7, 6, 5, 4, 3, 2, 1])
        y = np.array([9, 8, 7, 6, 5, 4, 3, 2, 1])
        x, y = np.meshgrid(x, y)
        z = x * y

        # z[z < -10] = np.nan  # get rid of missing data. pyvista needs you to do this

        i_res = 2  # display every nth point
        j_res = 2  # display every nth point
        self.grid = pv.StructuredGrid(x[::i_res, ::j_res], y[::i_res, ::j_res], z[::i_res, ::j_res])

        self.z = z
        self.x = x
        self.y = y

        self.plotter.add_mesh(self.grid, scalars=self.grid.points[:, 2], lighting=True, specular=0.5,
                              smooth_shading=True,
                              show_scalar_bar=True)

        if show:
            self.show()

    def add_sphere(self):  # changing resolution, not adding a sphere
        i_res = 5  # display every nth point
        j_res = 5  # display every nth point
        self.grid = pv.StructuredGrid(self.x[::i_res, ::j_res], self.y[::i_res, ::j_res], self.z[::i_res, ::j_res])
        self.plotter.update()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())