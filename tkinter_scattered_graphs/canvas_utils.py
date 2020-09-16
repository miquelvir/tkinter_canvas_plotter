from tkinter import Canvas

from tkinter_scattered_graphs.constants import SMALL_FONT


def dot(canvas: Canvas, x0: int, y0: int, radius: int = 1, fill_color="black", *args, **kwargs):
    x1, y1 = (x0 - radius), (y0 - radius)
    x2, y2 = (x0 + radius), (y0 + radius)
    canvas.create_oval(x1, y1, x2, y2, fill=fill_color, *args, **kwargs)


def tag_dot(canvas: Canvas, x0: int, y0: int, tag: str, radius: int = 1, fill_color="black", text_font=SMALL_FONT, *args, **kwargs):
    dot(canvas, x0, y0, radius=radius, fill_color=fill_color, *args, **kwargs)
    text(canvas, x0, y0, text=tag, font=text_font)


def text(canvas: Canvas, x0: int, y0: int, anchor: str = "nw", *args, **kwargs) -> None:
    """
    create a text

    default anchor nw sets x0, y0 to upper left corner
    """
    canvas.create_text(x0, y0, anchor=anchor, *args, **kwargs)


def rectangle(canvas: Canvas, x0: int, y0: int, width: int, height: int, fill="white", *args, **kwargs) -> None:
    """
    create a rectangle
    """
    canvas.create_rectangle(x0, y0, x0 + width, y0 + height, fill=fill, *args, **kwargs)
