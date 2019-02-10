import cv2
import numpy as np

from vision.rendering import draw_ellipse


def find_contours(segmentation):
    _, contours, _ = cv2.findContours(segmentation, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_L1)
    return contours


def ellipses_of_contour(contour):
    return cv2.fitEllipse(contour)


def shift_ellipses(ellipses, vec):
    (cx, cy), (x,y), angle = ellipses
    cx += vec[0]
    cy += vec[0]
    return (cx, cy), (x,y), angle


def attributes_of_ellipses(ellipses):
    cx,cy = ellipses[0]
    xax,yax = ellipses[1]
    angle = 90-ellipses[2]
    if angle < 0:
        angle = 360 + angle
    area = np.pi * xax * yax
    return (int(cx), int(cy)), (int(xax), int(yax)), angle, area


def area_of_ellipse(ellipse):
    _,_,_, area = attributes_of_ellipses(ellipse)
    return area


def is_bordertoucher(img, ellipse):
    dimensions = img.shape
    if len(dimensions) == 2:
        h, w = dimensions
    else:
        h, w, c = dimensions

    h_, w_ = int(h + 20), int(w + 20)
    xshift = int((h_ - h) / 2)
    yshift = int((w_ - w) / 2)

    ellipses_shifted = shift_ellipses(ellipse, (xshift, yshift))

    pad_blank = np.zeros((h_, w_))
    pad_w_ell = draw_ellipse(pad_blank, [ellipses_shifted], thickness=-1)
    pad_w_ell_rect = cv2.rectangle(pad_w_ell, (xshift, yshift), (xshift + h, yshift + w), thickness=-1, color=0)

    if (pad_w_ell_rect != 0).any():
        return True
    else:
        return False
