import json
import requests
import random
import torch
import json
import cv2
from vision.inference import run
from vision.evaluation import evalutate_once, init_dataset, init_model
from vision.geometry import attributes_of_ellipses

from io import BytesIO





data_dir = "/Users/lukassanner/Documents/ZeissHackathon/zeiss-lab/photomask_trainingdata"
model_path = "/Users/lukassanner/Documents/ZeissHackathon/zeiss-lab/vision/SlimWide_weakly_3.pth"

model = init_model(model_path)
ds = init_dataset(data_dir)

if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

BASE_URL = 'http://localhost:8000'

start_mask_response = requests.get(f'{BASE_URL}/masks/')
mask_id = start_mask_response.json()['count'] + 1

image_paths = range(1000)

mask_remaining = random.randint(10, 100)
position_remaining = random.randint(2, 4)
x_position = random.randint(10, 190)
y_position = random.randint(10, 190)
for k in range(len(ds)):
    imgs, ellipses, classes = evalutate_once(k, model, ds, device)
    print(imgs)
    buf = BytesIO()
    buf.write(cv2.imencode('.png', imgs)[1].tostring())

    files = {
        'image':  ('test.png', cv2.imencode('.png', imgs)[1].tostring())
    }


    data = []
    defects = []
    if ellipses:
        for e in ellipses:
            center, axis, angle, _ = attributes_of_ellipses(e)
            ellipse = {
                "ellipse": {
                    "centerX": center[0],
                    "centerY": center[1],
                    "x": axis[0],
                    "y": axis[1],
                    "rotation": angle
                }}

            defects.append(ellipse)

    if position_remaining == 0:
        if mask_remaining == 0:
            mask_id += 1
            mask_remaining = random.randint(10, 100)
        mask_remaining -= 1

        x_position = random.randint(10, 190)
        y_position = random.randint(10, 190)
        position_remaining = random.randint(2, 4)
    position_remaining -= 0


    data = {
        "mask_id": mask_id,
        "position_x": x_position,
        "position_y": y_position,
    }
    for i, d in enumerate(defects):
        data[f'new_defects[{i}]'] = json.dumps(d)


    print(data)
    print(files)

    response = requests.post(f'{BASE_URL}/defectpositionimages/', files=files,
                data=data)
    print(response.json())
    break
