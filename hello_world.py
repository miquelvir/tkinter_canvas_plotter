import tkinter as tk
from tk_scattered_graphs import MultidimensionalCorrelatedScatteredPlot, InvalidDatasetError

"""
This is boilerplate code for the use of tk_scattered_graphs package. 
A straight-forward hello-world like code to get a glance of how to use the package.
"""

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
FRAME_SIZE_PX = 20


def main():
    root = tk.Tk()
    root.geometry("{}x{}".format(WINDOW_WIDTH, WINDOW_HEIGHT))

    sample_data = [
            (6.08804, 3.457729, 2.34)
            , (5.275341, 6.538759, 1.11)
            , (4.184762, 5.221742, 1.23)
            , (0.678713, 0.951598, 2.45)
            , (-0.957855, 0.631947, 3.43)
            , (-0.131799, -0.324218, 1.23)
            , (-0.229171, 0.900907, 1.45)
    ]

    try:
        graphs = MultidimensionalCorrelatedScatteredPlot(sample_data, root,
                                                         WINDOW_WIDTH-FRAME_SIZE_PX,
                                                         WINDOW_HEIGHT-FRAME_SIZE_PX,
                                                         annotated_dots=False)  # set to true to display exact dot value
    except InvalidDatasetError:
        raise

    root.mainloop()


if __name__ == "__main__":
    main()
