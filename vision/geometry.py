import cv2
import numpy as np


def ellipses_of_contour(contour):
    return cv2.fitEllipse(contour)


def attributes_of_ellipses(ellipses):
    center = ellipses[0]
    axis = ellipses[1]
    angle = ellipses[2]
    area = np.pi * axis[0] * axis[1]
    return center, axis, angle, area


def is_bordertoucher(img, ellipse):
    dimensions = img.shape
    if len(dimensions) == 3:
        h, w, c = dimensions
    else:
        h, w = dimensions

    center, axis, angle, _ = attributes_of_ellipses(ellipse)

    cx, cy = center
    r = min(axis)
    R = max(axis)
    if cx + r >= w or cy + r >= h or cx - r <= 0 or cy-r <= 0:
        return True

    elif cx + R >= w or cy + R >= h or cx - R <= 0 or cy - R <= 0:
        return True
    
    else:
        return False

