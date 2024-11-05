from enum import Enum
import numpy as np

__all__ = ["Arrows"]


class Arrows(Enum):
    """
    An enum of chemfig-recognised arrow types.
    See p. 49 of http://ctan.imsc.res.in/macros/generic/chemfig/chemfig-en.pdf for
    visual examples.
    """

    forward = "->"
    backward = "<-"
    eq = "<=>"
    eq_fw = "<->>"
    eq_bw = "<<->"
    double = "<->"
    space = "0"
    split = "-U"


def orthogonal_line_points(x1, y1, x2, y2, length, ratio_intersection=0.5):
    # Calculate the midpoint of the original line
    mid_x = x1 + (x2 - x1) * ratio_intersection
    mid_y = y1 + (y2 - y1) * ratio_intersection

    # Calculate the slope of the original line
    dx = x2 - x1
    dy = y2 - y1

    # The slope of the orthogonal line is the negative reciprocal
    # dx and dy are swapped and one is negated to get an orthogonal direction
    orthogonal_dx = -dy
    orthogonal_dy = dx

    # Normalize the orthogonal direction to length 1
    length_scale = np.sqrt(orthogonal_dx**2 + orthogonal_dy**2)
    orthogonal_dx /= length_scale
    orthogonal_dy /= length_scale

    # Scale by the desired length
    orthogonal_dx *= length / 2
    orthogonal_dy *= length / 2

    # Calculate the two points of the orthogonal line
    orth_x1 = mid_x + orthogonal_dx
    orth_y1 = mid_y + orthogonal_dy
    orth_x2 = mid_x - orthogonal_dx
    orth_y2 = mid_y - orthogonal_dy

    return (orth_x1, orth_y1), (orth_x2, orth_y2)