import cv2
import torch
import numpy as np

def draw_ellipse(image, ellipses, thickness=2, color=(255,0,0)):
    out = image.copy()
    for ell in ellipses:
        cv2.ellipse(out, ell, color, thickness)
    return out


def back_tf(tensor):
    tensor = tensor.detach()
    tensor = torch.sigmoid(tensor)

    tensor *= 255
    tensor = tensor.int()
    return tensor.numpy().astype(np.uint8)