# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2016, wradlib Development Team. All Rights Reserved.
# Distributed under the MIT License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
#!/usr/bin/env python

import numpy as np

from vispy.scene import SceneCanvas
from vispy.util.event import EventEmitter
from vispy.visuals.transforms import STTransform
from vispy.scene.cameras import PanZoomCamera
from vispy.scene.visuals import Image, ColorBar, Markers, Text, Rectangle, Ellipse
from vispy.geometry import Rect

from wradvis import utils


class ColorbarCanvas(SceneCanvas):

    def __init__(self, **kwargs):
        super(ColorbarCanvas, self).__init__(keys='interactive', **kwargs)

        # set size ov Canvas
        self.size = 50, 450

        # unfreeze needed to add more elements
        self.unfreeze()

        # add grid central widget
        self.grid = self.central_widget.add_grid()

        # add view to grid
        self.view = self.grid.add_view(row=0, col=0)
        self.view.border_color = (0.5, 0.5, 0.5, 1)

        # initialize colormap, we take cubehelix for now
        # this is the most nice colormap for radar in vispy
        cmap = 'cubehelix'

        # initialize ColorBar Visual, add to view
        self.cbar = ColorBar(center_pos=(0, 10),
                             size=np.array([400, 20]),
                             cmap=cmap,
                             clim=(0, 255),
                             label_str='measurement units',
                             orientation='right',
                             border_width=1,
                             border_color='white',
                             parent=self.view.scene)

        # add transform to Colorbar
        self.cbar.transform = STTransform(scale=(1, 1, 1),
                                          translate=(20, 250, 0.5))

        # whiten label and ticks
        self.cbar.label.color = 'white'
        for tick in self.cbar.ticks:
            tick.color = 'white'

        self.freeze()


class RadolanCanvas(SceneCanvas):

    def __init__(self, **kwargs):
        super(RadolanCanvas, self).__init__(keys='interactive', **kwargs)

        # set size ov Canvas
        self.size = 450, 450

        # unfreeze needed to add more elements
        self.unfreeze()

        # add grid central widget
        self.grid = self.central_widget.add_grid()
        #self.view = self.central_widget.add_view()

        # add view to grid
        self.view = self.grid.add_view(row=0, col=0)
        self.view.border_color = (0.5, 0.5, 0.5, 1)

        # add signal emitters
        self.mouse_moved = EventEmitter(source=self, type="mouse_moved")

        # block double clicks
        self.events.mouse_double_click.block()

        # initialize empty RADOLAN image
        img_data = np.zeros((900, 900))

        # initialize colormap, we take cubehelix for now
        # this is the most nice colormap for radar in vispy
        cmap = 'cubehelix'

        # initialize Image Visual with img_data
        # add to view
        self.image = Image(img_data,
                           method='subdivide',
                           #interpolation='bicubic',
                           cmap=cmap,
                           parent=self.view.scene)

        # add transform to Image
        # (mostly positioning within canvas)
        self.image.transform = STTransform(translate=(0, 0, 0))

        # get radolan ll point coodinate into self.r0
        self.r0 = utils.get_radolan_origin()



        # create PanZoomCamera
        self.cam = PanZoomCamera(name="PanZoom",
                                 rect=Rect(0, 0, 900, 900),
                                 aspect=1,
                                 parent=self.view.scene)

        self.view.camera = self.cam

        self._mouse_position = None

        # create cities (Markers and Text Visuals
        self.create_cities()
        self.create_polygons()
        self.freeze()
        # print FPS to console, vispy SceneCanvas internal function
        self.measure_fps()

    def create_marker(self, id, pos, name):

        marker = Markers(parent=self.view.scene)
        marker.transform = STTransform(translate=(0, 0, -10))
        marker.interactive = True

        # add id
        marker.unfreeze()
        marker.id = id
        marker.freeze()

        marker.set_data(pos=pos[np.newaxis],
                        symbol="disc",
                        edge_color="blue",
                        face_color='red',
                        size=10)

        # initialize Markertext
        text = Text(text=name,
                     pos=pos,
                     font_size=15,
                     anchor_x='right',
                     anchor_y='top',
                     parent=self.view.scene)

        return marker, text


    def create_polygon(self, id, coords, name):
        pass




    def create_polygons(self):
        rect = Rectangle(center=(200, 200, 0), height=200.,
                                       width=300.,
                                       radius=[30., 30., 0., 0.],
                                       color=(0.5, 0.5, 0.2, 1),
                                       border_width=3,
                                       border_color='white', parent=self.view.scene)

        ellipse = Ellipse(center=(200, 200, 0), radius=(100, 150),
                                        color=(0.2, 0.2, 0.8, 1),
                                        border_color=(1, 1, 1, 1),
                                        border_width=3,
                                        start_angle=180., span_angle=150.,
                                        parent=self.view.scene)
        #rect.transforms = STTransform(translate=(0, 0, -5))

        #radolan = wrl.georef.create_osr('dwd-radolan')
        #path = '/automount/db01/python/data'
        #filename = 'ADM/germany/vg250_0101.gk3.shape.ebenen/vg250_ebenen/vg250_bld.shp'
        #dataset, inLayer = wrl.io.open_shape(os.path.join(path, filename))
        #borders, keys = wrl.georef.get_shape_coordinates(inLayer,
        #                                                 dest_srs=radolan)


        # print(borders[0], keys)
        # for brd in borders:
        #     if brd.ndim == 2:
        #         print(brd.shape)
        #         pos_scene = np.zeros((brd.shape[0], 2), dtype=np.float32)
        #         pos_scene[:] = brd - self.r0
        #         print(pos_scene.shape)
        #         print(pos_scene)
        #
        #         self.poly = Polygon([(0.4, 0.2), ],
        #                             color='red', border_color='white')
        #                             #border_width=3,
        #                             #parent=self.view.scene)
        #         self.poly.transform = STTransform(translate=(0, 0, -5))
        #         self.poly.interactive = True
        #         break
        #pass


    def create_cities(self):

        self.selected = None

        cities = utils.get_cities_coords()
        cnameList = []
        ccoordList = []
        for k, v in cities.items():
            cnameList.append(k)
            ccoordList.append(v)
        ccoord = np.vstack(ccoordList)
        ccoord = utils.wgs84_to_radolan(ccoord)
        pos_scene = np.zeros((ccoord.shape[0], 2), dtype=np.float32)
        pos_scene[:] = ccoord - self.r0

        # initialize Markers
        self.markers = []
        self.text = []
        i = 0
        for p, n in zip(pos_scene, cnameList):
            print(i, p, n)
            m, t = self.create_marker(i, p, n)
            self.markers.append(m)
            self.text.append(t)
            i += 1

    def on_mouse_move(self, event):
        point = self.scene.node_transform(self.image).map(event.pos)[:2]
        self._mouse_position = point
        # emit signal
        self.mouse_moved()

    def on_mouse_press(self, event):
        self.view.interactive = False

        for v in self.visuals_at(event.pos, radius=30):
            if isinstance(v, Markers):
                if self.selected is not None:
                    self.selected.symbol = 'disc'
                    if self.selected.id == v.id:
                        self.selected = None
                        break
                self.selected = v
                self.selected.symbol = 'star'
                print("Marker ID:", self.selected.id)

        self.view.interactive = True
