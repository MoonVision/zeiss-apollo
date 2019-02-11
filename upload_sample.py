import json
import requests
import random
import torch
import json
import cv2
import time
from random import shuffle
from vision.inference import run
from vision.evaluation import evalutate_once, init_dataset, init_model
from vision.geometry import attributes_of_ellipses

from io import BytesIO

BASE_URL = 'http://localhost:8000'

data_dir = "./Archive/photomask_trainingdata"
model_path = "./Archive/SlimWide_weakly_3.pth"

increase_factor = 1.3
current_min = 4
current_max = 6
mask_remaining = random.randint(3, 6)
position_remaining = random.randint(1, 2)
x_position = random.randint(10, 190)
y_position = random.randint(10, 190)
start_mask_response = requests.get(f'{BASE_URL}/masks/')
mask_id = start_mask_response.json()['count'] + 1
model = init_model(model_path)

if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

while(True):
    print('---------------------------------------RESTARTING----------------------------------')
    ds = init_dataset(data_dir)

    ds_range = [x for x in range(len(ds))]
    shuffle(ds_range)
    for k in ds_range:
        imgs, ellipses, classes = evalutate_once(k, model, ds, device)
        #print(imgs)
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

        if position_remaining <= 0:
            if mask_remaining <= 0:
                mask_id += 1
                current_min = int(current_min * increase_factor)
                current_max = int(current_max * increase_factor)
                mask_remaining = min(random.randint(current_min, current_max),
                        random.randint(100, 150))
            else:
                mask_remaining -= 1

            x_position = random.randint(10, 190)
            y_position = random.randint(10, 190)
            position_remaining = random.randint(1, 1)
        else:
            position_remaining -= 1

        data = {
            "mask_id": mask_id,
            "position_x": x_position,
            "position_y": y_position,
        }
        for i, d in enumerate(defects):
            data[f'new_defects[{i}]'] = json.dumps(d)

        print('~~~~~~~~~~~~~~~~~~~~~~~~Starting Upload~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(f'data {data}')
        #print(f'files {files}')
        response = requests.post(f'{BASE_URL}/defectpositionimages/', files=files,
                    data=data)
        print(f'Got response: {response.json()}')
        print('~~~~~~~~~~~~~~~~~~~~~~~~Upload Finished~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        time.sleep(.4)
