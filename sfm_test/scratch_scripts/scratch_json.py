# Trey Fortmuller

import numpy as np
import json

points = np.array([])


def add_to_list_of_lists(np_array, value):
    if len(np_array) == 0:
        np_array = np.append(np_array, [value])
    else:
        np_array = np.vstack((np_array, value))
    return np_array


# converting python dictionary data to json, writing to a file and saving it

rotation_mtx = [[1, 2, 3], [4, 5, 6], [7.0, 8.0, 9.0]]
center = [1, 2, 3]

extrinsics_data = [{"key": 0, "value": {"rotation": rotation_mtx, "center": center}}, {"key": 1, "value": {"rotation": rotation_mtx, "center": center}}]

with open('/home/trey.fortmuller/Desktop/sfm/SfM_test/scratch_data/new_sfm_data.json', 'r') as json_file:
    json_data = json.load(json_file)
    json_data['extrinsics'] = extrinsics_data

with open('/home/trey.fortmuller/Desktop/sfm/SfM_test/scratch_data/new_sfm_data.json', 'w') as json_file:
    json_file.write(json.dumps(json_data, indent=4))

# reading a json file and extracting data into a python dictionary
with open('/home/trey.fortmuller/Desktop/sfm/SfM_test/scratch_data/point_cloud.json') as json_file:
    data = json.load(json_file)
    for point in data["structure"]:
        # print("key number: " + str(point["key"]))
        coord = point["value"]["X"]
        points = add_to_list_of_lists(points, coord)

# print(points)
print(extrinsics_data)

# you can extend an empty python list (in place)
example = []
example.extend([1])
example.extend([2])
# print(example)  # [1, 2]
