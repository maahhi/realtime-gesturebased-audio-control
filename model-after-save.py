import pickle
import numpy as np
import pandas as pd

def body_preprocessing(class_gesture):
    df = pd.read_csv(class_gesture + '.csv')
    #combine index with heel and pinky with index
    print(df.columns)

    df['left_index_heel'] = df['left_index']
    df['left_pinky_index'] = df['left_pinky']
    df['right_index_heel'] = df['right_index']
    df['right_pinky_index'] = df['right_pinky']
    for i in range(df.shape[0]):
        li = eval(df['left_index'].iloc[i])
        lp = eval(df['left_pinky'].iloc[i])
        lip_str = "{'x':"+str(li['x']+lp['x'])+", 'y':"+str( li['y']+lp['y'])+"}"
        df['left_pinky_index'].iloc[i] = lip_str

        lh = eval(df['left_heel'].iloc[i])
        lfi = eval(df['left_foot_index'].iloc[i])
        lhi_str = "{'x':"+str(lh['x']+lfi['x'])+", 'y':"+str( lh['y']+lfi['y'])+"}"
        df['left_index_heel'].iloc[i] = lhi_str

        ri = eval(df['right_index'].iloc[i])
        rh = eval(df['right_heel'].iloc[i])
        rih_str = "{'x':"+str(ri['x']+rh['x'])+", 'y':"+str( ri['y']+rh['y'])+"}"
        df['right_index_heel'].iloc[i] = rih_str

        rp = eval(df['right_pinky'].iloc[i])
        rfi = eval(df['right_foot_index'].iloc[i])
        rpi_str = "{'x':"+str(rp['x']+rfi['x'])+", 'y':"+str( rp['y']+rfi['y'])+"}"
        df['right_pinky_index'].iloc[i] = rpi_str


    #drop the original columns
    df = df.drop(['left_index', 'left_heel', 'left_pinky', 'right_index', 'right_heel', 'right_pinky'], axis=1)

    X = np.zeros((df.shape[0],df.shape[1]*2))
    for i in range(df.shape[0]):
        for j,keyname in enumerate(df.columns):
            #str to dict
            position = eval(df[keyname].iloc[i])
            X[i][2 * j] = position['x']
            X[i][2 * j + 1] = position['y']
    return X




pos_class_gesture = 'gesture_class_0'#'M_openhands'
filename = pos_class_gesture + '_mlp_demo2.sav'
model = pickle.load(open(filename, 'rb'))
filename = pos_class_gesture + '_scaler_demo2.sav'
scaler = pickle.load(open(filename, 'rb'))

pos_class_gesture = 'am_ghezi'#'right_hand_up''M_openhands'
X_train = body_preprocessing(pos_class_gesture)
num_pos_class = X_train.shape[0]
# neg_class_gestures = ['gesture_class_1','gesture_class_2','gesture_class_3', 'gesture_class_4', 'gesture_class_5']
# #concatenate the negative class gestures
# a = X_train.shape[0]
# print('main class members',a)
"""
for neg_class_gesture in neg_class_gestures:
    X_train = np.concatenate((X_train, body_preprocessing(neg_class_gesture)), axis=0)
    b = X_train.shape[0]-a
    a = X_train.shape[0]
    print('negative class members',b)
#make the labels
Y_train = np.zeros(X_train.shape[0])
Y_train[:num_pos_class] = 1
"""

# y_train = np.zeros(X_train.shape[0])
# cls = 1
# last_len = X_train.shape[0]
# for neg_class_gesture in neg_class_gestures:
#     X_train = np.concatenate((X_train, body_preprocessing(neg_class_gesture)), axis=0)
#     y_train = np.concatenate((y_train, cls*np.ones(X_train.shape[0]-last_len)), axis=0)
#     print('main class members', X_train.shape[0]-last_len)
#     last_len = X_train.shape[0]
#     cls += 1


X_train = scaler.transform(X_train)
print(len(X_train[0]))
prediction = model.predict(X_train)
# print(y_train)
print("---------------")
print(prediction)