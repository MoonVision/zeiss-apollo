import torch
import numpy as np
import cv2
from PIL import Image
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
from torchvision.transforms import Compose
from torchvision import transforms

from vision.geometry import ellipses_of_contour, \
    area_of_ellipse, is_bordertoucher, find_contours

from vision.rendering import draw_ellipse, back_tf

def label_map(index):
    index = int(index)
    if index == 0:
        return 'COMPLETE FEATURE'
    elif index == 1:
        return 'BORDERTOUCHER'
    elif index == 2:
        return 'NO FEATURE'
    else:
        return 'unkown'


def get_propability(input, contour):
    mask = np.zeros(input.shape, dtype=np.int8)
    cv2.drawContours(mask, [contour], contourIdx=-1, color=True, thickness=-1)
    if len(contour) < 5:
        return 0
    else:
        el = ellipses_of_contour(contour=contour)
        area = area_of_ellipse(el)

        p = np.sum(input[mask]) / area
        return p

def threshold(image, thres):
    (t, segmentation) = cv2.threshold(image, thres, 255, cv2.THRESH_BINARY)
    return segmentation


def detect_features(im, probs, thres=200, min_prob=0.5):
    binary_segmentation = threshold(im, thres)
    contours = find_contours(binary_segmentation)

    propabilities = []
    ellipses = []
    border_checker = []

    if not contours:
        return ellipses, propabilities, border_checker
    largest_area = 0

    largest_contour = contours[-1]
    for c in contours:
        if len(c) > 5:
            area = cv2.contourArea(c)
            if area > largest_area:
                largest_area = area
                largest_contour = c

    # check for propability
    prob = get_propability(probs, largest_contour)

    if prob < min_prob:
        return [], [prob], [False]
    mask = np.zeros(im.shape)
    for c in contours:
        if len(c) > 6:
            ellipses.append(ellipses_of_contour(c))
            border_checker.append(is_bordertoucher(mask, ellipses[-1]))
            propabilities.append(prob)

    return ellipses, propabilities, border_checker


def annotate_prediction(im, detection):
    ellipses, propability, border_checker = detection
    annotated_im = im.copy()

    if ellipses:
        for ell, prob, border in zip(ellipses, propability, border_checker):
            if border:
                cv2.ellipse(annotated_im, ell, (0,255,0), -1)
            else:
                cv2.ellipse(annotated_im, ell, (255,0,0), 2)

    return np.concatenate([im, annotated_im])


def evalutate_once(index, model, ds, device):
    img, cls = ds[index]
    classes = []

    with torch.no_grad():
        pred = torch.nn.functional.upsample(model(img.unsqueeze(0)), scale_factor=(2, 2), mode="bilinear")
        pred = pred[0].squeeze()

    probs = 255* torch.sigmoid(pred).data.numpy()

    detection = detect_features(probs.astype(np.uint8), probs)
    #import pdb; pdb.set_trace()
    img_a = cv2.cvtColor(back_tf(img[0]), cv2.COLOR_GRAY2BGR)
    img_annotated = annotate_prediction(img_a, detection)

    ell, probs, border = detection
    if ell:
        ellipses = ell

        labels = []
        for b in border:
            if b:
                labels.append(label_map(1))
            else:
                labels.append(label_map(0))
        classes.append(labels)
    else:
        classes.append([label_map(2)])
        ellipses = None


    return img_annotated, ellipses, classes


def evaluate(model, ds, device):
    stacked_images = []
    ellipses_list = []
    classes = []

    for k in range(len(ds)):
        img, ellipes, cls = evalutate_once(k, model, ds, device)

        stacked_images.append(img)
        ellipses_list.append(ellipes)
        classes.append(cls)

    return stacked_images, ellipses_list, classes


def init_model(model_path):
    def map_location(storage, loc):
        return storage

    from vision.models import SlimWide
    m = SlimWide()
    m.load_state_dict(torch.load(model_path, map_location=map_location))
    m.eval()

    return m


def init_dataset(data_dir):
    from vision.data_prep import DataSubSet
    # We normalize to the mean dynamically

    def normalize_dynamic(tensor_img):
        mean = torch.mean(tensor_img)
        return (tensor_img - mean) / 0.1388

    ds = ImageFolder(data_dir)
    tf_eval = Compose([transforms.Grayscale(),
                       transforms.ToTensor(),
                       normalize_dynamic
                       ])
    indexes = np.arange(len(ds))

    ds_eval = DataSubSet(ds, [i for i in indexes], transform=tf_eval)

    return ds_eval


