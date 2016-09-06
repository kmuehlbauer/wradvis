# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2016, wradlib Development Team. All Rights Reserved.
# Distributed under the MIT License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
#!/usr/bin/env python


import numpy as np
import matplotlib
matplotlib.use('Qt4Agg')


from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from wradvis import utils

class MplCanvas(FigureCanvas):

    def __init__(self):#, parent, props):
        # plot definition
        self.fig = Figure()

        # initialization of the canvas
        FigureCanvas.__init__(self, self.fig)

        # we define the widget as expandable
        FigureCanvas.setSizePolicy(self,
        QtGui.QSizePolicy.Expanding,
        QtGui.QSizePolicy.Expanding)
        # notify the system of updated policy
        FigureCanvas.updateGeometry(self)

        self.ax = self.fig.add_subplot(111)
        grid = utils.get_radolan_grid()
        self.ax.pcolormesh(grid[..., 0], grid[..., 1], np.zeros((900,900)), vmin=0, vmax=255)
        self.ax.set_xlim([grid[..., 0].min(), grid[..., 0].max()])
        self.ax.set_ylim([grid[..., 1].min(), grid[..., 1].max()])


class MplWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.canvas = MplCanvas()
        self.vbl = QtGui.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

    def set_data(self, data):
        self.canvas.ax.collections[0].set_array(data[:-1, :-1].ravel())
        self.canvas.fig.canvas.draw()
