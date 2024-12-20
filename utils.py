import re

import matplotlib.pyplot as plt


def autolabel(rects):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    Parameters:
    rects (list): A list of rectangle objects (bars) to label.
    """
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
    """
    Convert a string to a float if possible, otherwise return the string.

    Parameters:
    text (str): The string to convert.

    Returns:
    float or str: The converted float value or the original string if conversion fails.
    """
    try:
        retval = float(text)
    except ValueError:
        retval = text
    return retval


def natural_keys(text):
    """
    Split a string into a list of floats and non-float substrings for natural sorting.

    Parameters:
    text (str): The string to split.

    Returns:
    list: A list of floats and non-float substrings.
    """
    return [atof(c) for c in re.split(r"[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)", text)]
