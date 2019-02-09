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