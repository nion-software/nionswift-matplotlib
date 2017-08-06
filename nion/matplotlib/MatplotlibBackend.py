"""A Matplotlib backend for drawing to a Nion Swift drawing context.

Using a display script, the following code will render a figure:

﻿import matplotlib
import matplotlib.figure
from nion.matplotlib import MatplotlibBackend
dpi = 72
figsize = bounds.width/dpi, bounds.height/dpi
figure = matplotlib.figure.Figure(figsize=figsize, dpi=dpi)
plot = figure.add_subplot(1, 1, 1)
plot.plot(display_data_and_metadata.data)
canvas = MatplotlibBackend.SwiftCanvas(figure)
canvas.draw()
canvas.render(drawing_context)
figure.clf()
"""

from nion.ui import DrawingContext

from matplotlib.backend_bases import RendererBase, GraphicsContextBase, FigureCanvasBase
from matplotlib.path import Path

import numpy


class SwiftRenderer(RendererBase):
    def __init__(self, drawing_context: DrawingContext.DrawingContext, height, font_metrics_fn):
        super().__init__()
        self.__drawing_context = drawing_context
        self.__get_font_metrics_fn = font_metrics_fn
        self.__height = height

    def __setup_color(self, rgb_a):
        if len(rgb_a) == 3:
            rgb_a = rgb_a + (1)
        rgb_a = tuple([int(com * 255) for com in rgb_a[:3]]) + tuple([rgb_a[3]])
        return "rgba({}, {}, {}, {})".format(*rgb_a)

    def draw_path(self, gc: GraphicsContextBase, path: Path, transform, rgbFace=None):
        # if path.codes is not None:
        self.__drawing_context.begin_path()
        for vertex, code in path.iter_segments(simplify=False, curves=True):
            if code == Path.MOVETO:
                point = transform.transform_point(vertex)
                self.__drawing_context.move_to(point[0], self.__height - point[1])
            elif code == Path.LINETO:
                point = transform.transform_point(vertex)
                self.__drawing_context.line_to(point[0], self.__height - point[1])
            elif code == Path.CLOSEPOLY:
                self.__drawing_context.close_path()
            elif code == Path.CURVE4:
                cpoint0 = transform.transform_point(vertex[0:2])
                cpoint1 = transform.transform_point(vertex[2:4])
                endpoint = transform.transform_point(vertex[4:])
                self.__drawing_context.bezier_curve_to(cpoint0[0], self.__height - cpoint0[1], cpoint1[0], self.__height - cpoint1[1], endpoint[0], self.__height - endpoint[1])
            elif code == Path.CURVE3:
                cpoint0 = transform.transform_point(vertex[0:2])
                endpoint = transform.transform_point(vertex[2:])
                self.__drawing_context.quadratic_curve_to(cpoint0[0], self.__height - cpoint0[1], endpoint[0], self.__height - endpoint[1])
        if rgbFace is not None:
            self.__drawing_context.fill_style = self.__setup_color(rgbFace)
            self.__drawing_context.fill()
        self.__drawing_context.line_width = self.points_to_pixels(gc.get_linewidth())
        self.__drawing_context.stroke_style = self.__setup_color(gc.get_rgb())
        self.__drawing_context.stroke()

    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        y = self.__height - y
        self.__drawing_context.save()
        self.__drawing_context.translate(x, y)
        self.__drawing_context.rotate(-numpy.deg2rad(angle))
        self.__drawing_context.translate(-x, -y)
        self.__drawing_context.fill_style = self.__setup_color(gc.get_rgb())
        self.__drawing_context.fill_text(s, x, y)
        self.__drawing_context.restore()

    def draw_image(self, gc, x, y, im, transform=None):
        self.__drawing_context.draw_image(im, x, self.__height - y, 0, 0)

    def flipy(self):
        return False

    def new_gc(self):
        return GraphicsContextBase()

    @staticmethod
    def get_font_from_props(prop):
        # "normal 11px serif"
        return "{} {}px {}".format(prop.get_slant(), prop.get_size(), prop.get_family()[0])

    def get_text_width_height_descent(self, s, prop, ismath=False):
        font_metrics = self.__get_font_metrics_fn(SwiftRenderer.get_font_from_props(prop), s)
        return font_metrics.width, font_metrics.height, font_metrics.descent


class SwiftCanvas(FigureCanvasBase):
    def __init__(self, figure, get_font_metrics_fn):
        super().__init__(figure)
        self.__drawing_context = DrawingContext.DrawingContext()
        self.__get_font_metrics_fn = get_font_metrics_fn

    def draw(self):
        renderer = SwiftRenderer(self.__drawing_context, self.figure.get_figheight() * self.figure.get_dpi(), self.__get_font_metrics_fn)
        self.figure.draw(renderer)

    def render(self, drawing_context: DrawingContext.DrawingContext):
        drawing_context.add(self.__drawing_context)
