import json
import pandas as pd


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

def bodyfeatures(filename):
    print('filename:',filename)
    pairs = ['shoulder', 'elbow', 'wrist', 'pinky', 'index', 'hip', 'knee', 'heel', 'foot_index']

    #concat 2 list


    columns = ['nose'] + ['left_' + l for l in pairs]+ ['right_' + r for r in pairs]
    df = pd.DataFrame(columns=columns)
    print(df.columns.tolist(),columns)


    rawdata=load_json_objects(filename+'.json')
    for i,obj in enumerate(rawdata):
        row_data = {}
        if (len(obj) != 0):
            for LRN_key in obj.keys():
                for bodypart in obj[LRN_key]:
                    if bodypart in df.columns.tolist():
                        row_data.update({bodypart : obj[LRN_key][bodypart]})
        #add a dictionary with same keys as columns to a data
        ndf = pd.DataFrame([row_data])
        df = pd.concat([df, ndf])
    print(filename,len(df))
    return df


def bodygesture_jsontocsv(gesture_name):
    bfdf = bodyfeatures(gesture_name)

    #print(bfdf.head())
    #is there any missing data?
    #print(bfdf.isnull().sum())
    print('done')
    #save to csv
    bfdf.to_csv(gesture_name+'.csv',index=False)
# bg = ['a_right_hand_up','a_right_leg_up','a_left_hand_up','a_left_leg_up','a_nutral_stand']
# bg = ['gesture_class_0', 'gesture_class_1', 'gesture_class_2', 'gesture_class_3', 'gesture_class_4', 'gesture_class_5']
bg = ["am_ghezi"]
for i in range(len(bg)):
    print(bg[i])
    bodygesture_jsontocsv(bg[i])
