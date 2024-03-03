import re

import matplotlib.pyplot as plt


def autolabel(rects):
    xpos = "center"
    ha = {"center": "center", "right": "left", "left": "right"}
    offset = {"center": 0.5, "right": 0.57, "left": 0.43}

    for rect in rects:
        height = rect.get_height()
        plt.text(
            rect.get_x() + rect.get_width() * offset[xpos],
            1.01 * height,
            "{}".format(height),
            ha=ha[xpos],
            va="bottom",
        )


def atof(text):
    try:
        retval = float(text)
    except ValueError:
        retval = text
    return retval


def natural_keys(text):
    return [atof(c) for c in re.split(r"[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)", text)]
