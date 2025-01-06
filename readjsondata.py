import json
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Or 'Agg' if you don't need to display the plot
import numpy as np
from scipy.ndimage import gaussian_filter1d

import pandas as pd

np.random.seed(0)

def exponential_moving_average(data, alpha=0.1):
    smoothed = [data[0]]
    for i in range(1, len(data)):
        smoothed.append(alpha * data[i] + (1 - alpha) * smoothed[i-1])
    return smoothed

with open('X_true.json', 'r') as file:
    X_true = json.load(file)
    print(type(X_true))
    print(type(X_true[0][0][0][0]))

with open('X_false.json', 'r') as file:
    X_false = json.load(file)


#[Rwrist[X, Y, Z], Relbow[X, Y, Z], Rshoulder[X, Y, Z]]
print(len(X_true))
print(len(X_false))
for i in range(len(X_true)):
    sample = X_true[i]
    Rwrist = sample[0]
    Relbow = sample[1]
    Rshoulder = sample[2]
    print(len(Rwrist[0]))


for i in range(len(X_false)):
    sample = X_true[i]
    Rwrist = sample[0]
    Relbow = sample[1]
    Rshoulder = sample[2]
    print(len(Rwrist[0]))

print(X_true[0])
df_x_true = pd.DataFrame(columns=['RwristX','RwristY','RwristZ','RelbowX','RelbowY','RelbowZ','RshoulderX','RshoulderY','RshoulderZ'])
for i, row in enumerate(X_true):
    df_x_true.loc[i]=[row[0][0], row[0][1], row[0][2], row[1][0], row[1][1], row[1][2], row[2][0], row[2][1], row[2][2]]

print(df_x_true.head())
print(len(df_x_true))

RwristY=[]
for i in range(len(X_true)):
    RwristY.append(X_true[i][0][1]) # RwristY


#padding
# Padding series to the length of the longest one
max_length = max(len(series) for series in RwristY)
for i, series in enumerate(RwristY):
    RwristY[i] = series + [None] * (max_length - len(series))


print(RwristY[10])
time = range(len(RwristY[10]))
numeric_data = np.array(RwristY[10], dtype=float)  # Ensure data is numeric
smooth = gaussian_filter1d(numeric_data, sigma=1)
EMA = exponential_moving_average(numeric_data, alpha=0.1)

print(smooth)
plt.plot(time, RwristY[10], label='RwristY')
#plt.plot(time, smooth, label='Smoothed RwristY')
#plt.plot(time, EMA, label='Exponential Moving Average RwristY')

# Display the plot
plt.show()
