import tkinter as tk

from typing import Tuple, List

from tk_scattered_graphs.canvas_utils import dot, rectangle, tag_dot, text
from tk_scattered_graphs.constants import MED_SPACE_PX

OUTLINE_COLOR = "black"
AXIS_SPACE_PX = MED_SPACE_PX
DOT_RADIUS_PX = 3


class TwoDimensionsScatteredPlot:
    def __init__(self, data: List[Tuple[float, float]], canvas: tk.Canvas, x0, y0, plot_width, plot_height, annotated_dots=False):
        """ initialise a two dimensional scattered plot """

        self._data: List[Tuple[float, float]] = data
        self._canvas = canvas
        self._x0, self._y0 = x0, y0
        self._width, self._height = plot_width, plot_height

        # get current configuration according to initialization values
        self._plot_width, self._plot_height = self._get_plot_dimensions()
        self._min_x, self._min_y, self._max_x, self._max_y = self._get_data_boundaries()
        self._plot_x0, self._plot_y0 = self._get_plot_coordinates()
        self._x_factor = self._get_factor(self._min_x, self._max_x, self._plot_width)
        self._y_factor = self._get_factor(self._min_y, self._max_y, self._plot_height)

        # draw the plot frame
        self._set_frame()

        # draw the plot values
        self._plot_points(annotated_dots)

        # write the reference measures
        self._set_measure_indications()

    def _plot_points(self, tags: bool = False):
        """ for each point in self._data, plot it (with a tag if tags) """
        for point in self._data:
            if tags:
                tag_dot(self._canvas, *self._get_px(point), tag=str(point), radius=DOT_RADIUS_PX)
            else:
                dot(self._canvas, *self._get_px(point), radius=DOT_RADIUS_PX)

    @staticmethod
    def _get_factor(min_: float, max_: float, px_size: int):
        """
        given the minimum and maximum values to represent, as well as the pixels available, returns
        a conversion factors from values to represent to pixels
        """
        range_ = abs(max_ - min_)
        return px_size / range_ if range_ != 0 else 1  # if we only need to represent 1 pixel, we can use 1 as density

    def _get_px(self, point: Tuple[float, float]) -> Tuple[int, int]:
        """
        given an x value, computes which canvas coordinate it must have using a conversion factor

        displacement_from_origin = abs(x_value - min_x) [in the represented values scale]
        real_px = origin_of_coordinates + displacement_from_origin * x_conversion_factor [transformed to pixels]
        """
        x = round(self._plot_x0 + abs(point[0] - self._min_x) * self._x_factor)

        """
        self._plot_height and the minus signs are needed to compute the y pixel, because
        tkinter coordinate system has y=0 at the top, and we have y=0 at the bottom
        """
        y = round(self._plot_y0 + self._plot_height - abs(point[1] - self._min_y) * self._y_factor)
        return x, y

    def _get_data_boundaries(self) -> Tuple[float, float, float, float]:
        """ get min and max x and y """
        max_x, max_y = tuple(map(max, zip(*self._data)))
        min_x, min_y = tuple(map(min, zip(*self._data)))
        return min_x, min_y, max_x, max_y

    def _get_plot_dimensions(self) -> Tuple[int, int]:
        """ get usable plot size (total size - axis reserved space) """
        return self._width - AXIS_SPACE_PX, self._height - AXIS_SPACE_PX

    def _get_plot_coordinates(self) -> Tuple[int, int]:
        """ get x0, y0 coordinates of the plot space """
        return self._x0 + AXIS_SPACE_PX, self._y0  # y does not need to be added AXIS_SPACE_PX, since it is at bottom

    def _set_frame(self):
        """ draw a frame for the plot space (excluding the axis reserved space) """
        rectangle(self._canvas, self._plot_x0, self._plot_y0, self._plot_width, self._plot_height, outline=OUTLINE_COLOR)

    def _set_measure_indications(self):
        """ adds min and max measures in the axis """

        # x axis
        text(self._canvas, self._plot_x0, self._plot_y0 + self._plot_height, text=str(self._min_x))
        text(self._canvas, self._plot_x0 + self._plot_width, self._plot_y0 + self._plot_height, text=str(self._max_x), anchor="ne")

        # y axis
        text(self._canvas, self._plot_x0, self._plot_y0 + self._plot_height, text=str(self._min_y), angle=90, anchor="sw")
        text(self._canvas, self._plot_x0, self._plot_y0, text=str(self._max_y), angle=90, anchor="se")