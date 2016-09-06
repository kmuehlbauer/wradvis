# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2016, wradlib Development Team. All Rights Reserved.
# Distributed under the MIT License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
#!/usr/bin/env python

from PyQt4 import QtGui, QtCore

# other wradvis imports
from wradvis.glcanvas import RadolanWidget, RadolanCanvas, ColorbarCanvas
from wradvis.mplcanvas import MplWidget
from wradvis.properties import PropertiesWidget
from wradvis import utils


class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.resize(825, 500)
        self.setWindowTitle('RADOLAN Viewer')
        self._need_canvas_refresh = False

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.reload)

        # initialize RadolanCanvas
        self.rcanvas = RadolanWidget()
        self.canvas = self.rcanvas

        # initialize MplWidget
        self.mcanvas = MplWidget()

        # canvas swapper
        self.swapper = []
        self.swapper.append(self.rcanvas)
        self.swapper.append(self.mcanvas)

        # add PropertiesWidget
        self.props = PropertiesWidget()
        self.props.signal_slider_changed.connect(self.slider_changed)
        self.props.signal_playpause_changed.connect(self.start_stop)
        self.props.signal_speed_changed.connect(self.speed)

        # add Horizontal Splitter andd the three widgets
        self.splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.splitter.addWidget(self.props)
        self.splitter.addWidget(self.swapper[0])#.native)
        self.splitter.addWidget(self.swapper[1])
        self.swapper[1].hide()
        self.setCentralWidget(self.splitter)

        # finish init
        self.slider_changed()

    def reload(self):
        if self.props.slider.value() == self.props.slider.maximum():
            self.props.slider.setValue(1)
        else:
            self.props.slider.setValue(self.props.slider.value() + 1)

    def start_stop(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start()

    def speed(self):
        self.timer.setInterval(self.props.speed.value())

    def slider_changed(self):
        self.data, self.meta = utils.read_radolan(self.props.filelist[self.props.actualFrame])
        scantime = self.meta['datetime']
        print(scantime)

        self.props.sliderLabel.setText(scantime.strftime("%H:%M"))
        self.props.date.setText(scantime.strftime("%Y-%m-%d"))
        self.canvas.set_data(self.data)


    def mouse_moved(self, event):
        self.props.show_mouse(self.canvas._mouse_position)

    def keyPressEvent(self, event):
        #QtGui.QMessageBox.information(None, "Received Key Press Event!!",
        #                        "You Pressed: " + event.text())
        if event.text() == 'c':
            self.swapper = self.swapper[::-1]
            self.canvas = self.swapper[0]
            self.swapper[0].show()
            self.swapper[1].hide()


def start(arg):
    appQt = QtGui.QApplication(arg.argv)
    win = MainWindow()
    win.show()
    appQt.exec_()

if __name__ == '__main__':
    print('wradview: Calling module <gui> as main...')
