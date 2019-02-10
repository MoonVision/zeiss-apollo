import json
import requests
import random

BASE_URL = 'http://localhost:8000'

data = {
    "mask_id": 1,
    "position_x": 100,
    "position_y": 120,
    "new_defects": json.dumps([
        {
            "ellipse": {
                "centerX": 123,
                "centerY": 234,
                "x": 1,
                "y": 2,
                "rotation": 34.3
            }
        }
    ])
}
files = {
    'image': open('/Users/mattnicolls/Downloads/zeiss_sample_2.tif', 'rb'),
}
response = requests.post(f'{BASE_URL}/defectpositionimages/', files=files, data=data)
print(response.json())











'''
start_mask_response = requests.get(f'{BASE_URL}/masks/')
mask_id = start_mask_response.json()['count'] + 1

image_paths = range(1000)

mask_remaining = random.randint(10, 100)
position_remaining = random.randint(2, 4)
x_position = random.randint(10, 190)
y_position = random.randint(10, 190)
for image_path in image_paths:
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
        "defect_x": x_position,
        "defect_y": y_position,
        "defects": json.dumps([
            {
                "ellipse": {
                    "centerX": 123,
                    "centerY": 234,
                    "x": 1,
                    "y": 2,
                    "rotation": 34.3
                }
            }
        ])
    }
    files = {
        'image': open('/Users/mattnicolls/Downloads/zeiss_sample_2.tif', 'rb'), # TODO: replace with image_path
    }
    print(data)
    print(files)
    response = requests.post(f'{BASE_URL}/defectpositionimages/', files=files,
                data=data)
    print(response.json())
    break
'''
