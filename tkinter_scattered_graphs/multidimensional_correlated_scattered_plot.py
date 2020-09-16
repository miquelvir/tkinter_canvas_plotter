import tkinter as tk

from typing import List, Tuple
from math import floor

from tkinter_scattered_graphs.errors import InvalidDatasetError
from tkinter_scattered_graphs.two_dimensions_scattered_plot import TwoDimensionsScatteredPlot
from tkinter_scattered_graphs.canvas_utils import text
from tkinter_scattered_graphs.constants import *

EXTERIOR_MARGIN_PX = MED_SPACE_PX
TAG_SPACE_PX = MED_SPACE_PX
INTERIOR_MARGIN_PX = MIN_SPACE_PX
TITLE_SPACE_PX = MED_SPACE_PX + 5
DESCRIPTION_SPACE_PX = TAG_SPACE_PX
DESCRIPTION_LOWER_MARGIN_PX = MIN_SPACE_PX
HEADER_SPACE_PX = TITLE_SPACE_PX + DESCRIPTION_SPACE_PX + DESCRIPTION_LOWER_MARGIN_PX



"""
NOTE
object coordinates are given as the upper-left corner coordinates
"""


class MultidimensionalCorrelatedScatteredPlot:
    """
    creates a multidimensional correlated scattered plot using some two dimensional scattered plots

    variables are distributed as follows:

    ...     ...
    (0,1)   (1,1)   ...
    (0,0)   (1,0)   ...

    """

    def __init__(self, data: List[tuple], root: tk.Tk, width: int, height: int, bg: str = "white",
                 title: str = "my n-dimension correlated plot",
                 description: str = "this plot can have n > 1 variables; it uses a correlated plot system to visualize the multiple dimensions",
                 annotated_dots=False):
        if len(data) == 0 or len(data[0]) <= 1:  # at least one point, at least 2 dimensions
            raise InvalidDatasetError

        self.data = data
        self.width, self.height = width, height
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg=bg)  # create base canvas

        # get settings for current initialization
        variable_count = self._get_variable_count()
        plot_width, plot_height = self._get_individual_plot_dimensions(variable_count)

        # draw texts for title, description and axis tags
        self._set_title(title)
        self._set_description(description)
        self._set_variable_tags(variable_count, plot_width, plot_height)

        # draw plots

        for variable_x in range(variable_count):  # plot each variable in the x row
            for variable_y in range(variable_count):  # plot the column
                dataset_to_plot = self._get_dataset_for_variables(variable_x, variable_y)
                x0, y0 = self._get_plot_coordinates(variable_x, variable_y, plot_width, plot_height)
                TwoDimensionsScatteredPlot(dataset_to_plot, self.canvas, x0, y0, plot_width, plot_height,
                                           annotated_dots=annotated_dots)

        # pack to root
        self.canvas.pack()

    def _get_individual_plot_dimensions(self, variable_count) -> Tuple[int, int]:
        """
        get the individual graph size we can allocate

        from the total width/height, we must leave:
                + EXTERIOR_MARGIN_PX of padding at each side
                + LABEL_SPACE_PX space for variable label
                + INTERIOR_MARGIN_PX between individual plots
                = 2 * MED_MARGIN_PX + LABEL_SPACE_PX + (variable_count - 1) * INTERIOR_MARGIN_PX

        height must leave additional TITLE_SPACE_PX + DESCRIPTION_SPACE_PX + TITLE_UPPER_MARGIN_PX for the title and description

        :return: plot_width, plot_height
        """

        # usable = total - margins - variable label space - between plots separation
        default_margins = 2 * EXTERIOR_MARGIN_PX + 1 * TAG_SPACE_PX + (variable_count - 1) * INTERIOR_MARGIN_PX
        usable_width = self.width - default_margins
        usable_height = self.height - default_margins - TITLE_SPACE_PX - DESCRIPTION_SPACE_PX - DESCRIPTION_LOWER_MARGIN_PX  # subtract space for title and description

        # from the usable size, get the size  allocated for each individual plot
        plot_width = floor(usable_width / variable_count)
        plot_height = floor(usable_height / variable_count)

        return plot_width, plot_height

    def _get_plot_coordinates(self, variable_x, variable_y, plot_width, plot_height) -> Tuple[int, int]:
        x0 = EXTERIOR_MARGIN_PX + TAG_SPACE_PX  # padding and var labels
        if variable_x != 0:  # add the space of each plot to its left and interior margin
            x0 += (plot_width + INTERIOR_MARGIN_PX) * variable_x

        y0 = self.height - TAG_SPACE_PX - EXTERIOR_MARGIN_PX - plot_height  # title & description, padding and var labels
        if variable_y != 0:  # add the space of each plot on top of it and interior margin
            y0 -= (plot_height + INTERIOR_MARGIN_PX) * variable_y

        return x0, y0

    @staticmethod
    def _get_title_coordinates():
        return EXTERIOR_MARGIN_PX, EXTERIOR_MARGIN_PX

    def _set_title(self, title: str) -> None:
        x0, y0 = self._get_title_coordinates()
        text(self.canvas, x0, y0, fill=TEXT_COLOR, font=H1_FONT, text=title)

    @staticmethod
    def _get_description_coordinates():
        return EXTERIOR_MARGIN_PX, EXTERIOR_MARGIN_PX + TITLE_SPACE_PX

    def _set_description(self, description: str) -> None:
        x0, y0 = self._get_description_coordinates()
        text(self.canvas, x0, y0, fill=TEXT_COLOR, font=P_FONT, text=description)

    def _set_variable_tags(self, variable_count: int, plot_width: int, plot_height: int) -> None:
        """ write variable tags for each variable, in the x and y axis """
        def get_variable_tags_y_axis_x0_coordinate():
            return EXTERIOR_MARGIN_PX

        def get_variable_tags_x_axis_y0_coordinate(height_: int):
            y0_ = height_ - EXTERIOR_MARGIN_PX - TAG_SPACE_PX
            return y0_

        def get_variable_tag_x_axis_coordinates(variable_number_, plot_width_, x_axis_y0_):
            return EXTERIOR_MARGIN_PX + TAG_SPACE_PX + (plot_width_ + INTERIOR_MARGIN_PX) * variable_number_, \
                   x_axis_y0_

        def get_variable_tag_y_axis_coordinates(variable_number_, plot_height_, y_axis_x0_):
            return y_axis_x0_, \
                   self.height - (EXTERIOR_MARGIN_PX + TAG_SPACE_PX + (plot_height_ + INTERIOR_MARGIN_PX) * variable_number_)

        # use default literal dimension names until dimension 4, numbers otherwise
        if variable_count <= 4:
            tags = ["x", "y", "z", "t"][:variable_count]
        else:
            tags = ["dim{}".format(dim) for dim in range(variable_count)]

        y_axis_x0 = get_variable_tags_y_axis_x0_coordinate()
        x_axis_y0 = get_variable_tags_x_axis_y0_coordinate(self.height)

        for variable_number, tag in enumerate(tags):
            # tag in the x axis
            x0, y0 = get_variable_tag_x_axis_coordinates(variable_number, plot_width, x_axis_y0)
            text(self.canvas, x0, y0, fill=TEXT_COLOR, font=P_FONT, text=tag)

            # tag in the y axis, angle property in text() is used to have tags as vertical text
            x0, y0 = get_variable_tag_y_axis_coordinates(variable_number, plot_height, y_axis_x0)
            text(self.canvas, x0, y0, fill=TEXT_COLOR, font=P_FONT, text=tag, angle=90)

    def _get_variable_count(self) -> int:
        return len(self.data[0])  # get the number of variables from the first point

    def _get_dataset_for_variables(self, variable_x: int, variable_y: int) -> List[tuple]:
        # get for each point, a new point with the desired variables
        return [(point[variable_x], point[variable_y]) for point in self.data]

