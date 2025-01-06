import json


def load_json_objects(filename):
    with open(filename, 'r') as file:
        content = file.read()

    objects = []
    obj_buffer = ''
    brace_count = 0
    in_object = False

    for char in content:
        if char == '{':
            brace_count += 1
            in_object = True
        elif char == '}':
            brace_count -= 1

        if in_object:
            obj_buffer += char

        # Check if we've reached the end of a JSON object
        if in_object and brace_count == 0:
            try:
                # Parse the JSON object
                json_obj = json.loads(obj_buffer)
                objects.append(json_obj)
            except json.JSONDecodeError:
                print("Error decoding JSON object.")

            # Reset buffer and in_object flag for the next JSON object
            obj_buffer = ''
            in_object = False

    return objects


# Usage example
gesture_counter = {}
filename = 'data-700ish.json'
json_objects = load_json_objects(filename)
counter = 0

print(list(json_objects[10]['Right'].keys()))
"""
for obj in json_objects:
    if(len(obj) != 0):
        counter+= 1
        left_right_key = list(obj.keys())[0]
        gesture = list(obj[left_right_key]['Gestures'].keys())[0]
        if gesture in gesture_counter:
            gesture_counter[gesture] += 1
        else:
            gesture_counter[gesture] = 1
        print(left_right_key,',',gesture)
print(len(json_objects))
print(gesture_counter)
"""

# make a dataframe based on json
import pandas as pd
import numpy as np

columns = ['Left','Gestures', 'index_finger_dip', 'index_finger_mcp', 'index_finger_pip', 'index_finger_tip', 'middle_finger_dip', 'middle_finger_mcp', 'middle_finger_pip', 'middle_finger_tip', 'pinky_finger_dip', 'pinky_finger_mcp', 'pinky_finger_pip', 'pinky_finger_tip', 'ring_finger_dip', 'ring_finger_mcp', 'ring_finger_pip', 'ring_finger_tip', 'thumb_cmc', 'thumb_ip', 'thumb_mcp', 'thumb_tip', 'wrist']
df = pd.DataFrame(columns=columns)

for obj in json_objects:
    if(len(obj) != 0):
        left_right_key = list(obj.keys())[0]
        left_right_value = 1
        if left_right_key == 'Right':
            left_right_value = 0
        values = obj[left_right_key]
        df.loc[len(df)] = values
        df.loc[len(df)-1, 'Left'] = left_right_value

print(df.loc[0])
"""
#save the dataframe to a csv file
df.to_csv('data.csv', index=False)
print('done')
"""