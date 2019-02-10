import json
import requests
import random
import torch
import json

from vision.inference import run
from vision.evaluation import evalutate_once, init_dataset, init_model
from vision.geometry import attributes_of_ellipses

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


for k in len(ds):
    imgs, ellipses, classes = evalutate_once(k, model, ds, device)

    files = {
        'image': imgs
    }

    defects = []
    data = []

    if ellipses:
        for e in ellipses:
            center, axis, angle,_ = attributes_of_ellipses(e)
            ellipse = {
                "ellipse": {
                    "centerX": center[0],
                    "centerY": center[1],
                    "x": axis[0],
                    "y": axis[1],
                    "rotation": angle
                }}

            defects.append(ellipse)

    for i, d in enumerate(defects):
        data[f'new_defects[{i}]'] = json.dumps(d)

    print(data)
    response = requests.post(f'{BASE_URL}/defectpositionimages/', files=files,data=data)
    print(response.json())
    break

