import cv2


def draw_ellipse(image, ellipses, thickness=2, color=(255,0,0)):
    out = image.copy()
    for ell in ellipses:
        cv2.ellipse(out, ell, color, thickness)
    return out