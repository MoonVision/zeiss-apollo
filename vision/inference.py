import torch
import cv2

import vision.evaluation as eval


def run(data_dir, model_dir):
    model = eval.init_model(model_dir)
    ds = eval.init_dataset(data_dir)

    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")

    images, ellipses, classes = eval.evaluate(model, ds, device)

    return images, ellipses, classes


if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser(description='ZEISS Lab training')

    parser.add_argument("-i", "--in-data", required=True)
    parser.add_argument("-m", "--model-dir", required=True)

    opt = parser.parse_args()

    images, ellipses, classes = run(opt.in_data, opt.model_dir)

    for im in images:
        cv2.imshow('evaluation', im)
        cv2.waitKey(0)
