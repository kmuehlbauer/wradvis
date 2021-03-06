# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2016, wradlib Development Team. All Rights Reserved.
# Distributed under the MIT License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
#!/usr/bin/env python

from PyQt4 import QtGui, QtCore

# other wradvis imports
from wradvis.glcanvas import RadolanCanvas, ColorbarCanvas
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
        self.canvas = RadolanCanvas()
        self.canvas.create_native()
        self.canvas.native.setParent(self)

        # need some tracer for the mouse position
        self.canvas.mouse_moved.connect(self.mouse_moved)

        # add ColorbarCanvas
        self.canvas_cb = ColorbarCanvas()
        self.canvas_cb.create_native()
        self.canvas_cb.native.setParent(self)

        # add PropertiesWidget
        self.props = PropertiesWidget()
        self.props.signal_slider_changed.connect(self.slider_changed)
        self.props.signal_playpause_changed.connect(self.start_stop)
        self.props.signal_speed_changed.connect(self.speed)

        # add Horizontal Splitter andd the three widgets
        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self.props)
        splitter.addWidget(self.canvas.native)
        splitter.addWidget(self.canvas_cb.native)
        self.setCentralWidget(splitter)

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
        self.props.sliderLabel.setText(scantime.strftime("%H:%M"))
        self.props.date.setText(scantime.strftime("%Y-%m-%d"))
        self.canvas.image.set_data(self.data)
        self.canvas.update()

    def mouse_moved(self, event):
        self.props.show_mouse(self.canvas._mouse_position)


def start(arg):
    appQt = QtGui.QApplication(arg.argv)
    win = MainWindow()
    win.show()
    appQt.exec_()

if __name__ == '__main__':
    print('wradview: Calling module <gui> as main...')
