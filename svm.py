from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

import json
import pandas as pd
import numpy as np

with open('X_true.json', 'r') as file:
    X_true = json.load(file)
with open('X_false.json', 'r') as file:
    X_false = json.load(file)

min_samples_size = min(len(X_true[0][0][0]), len(X_true[0][0][0]))

df_x_true = pd.DataFrame(columns=['RwristX','RwristY','RwristZ','RelbowX','RelbowY','RelbowZ','RshoulderX','RshoulderY','RshoulderZ'])
df_x_false = pd.DataFrame(columns=['RwristX','RwristY','RwristZ','RelbowX','RelbowY','RelbowZ','RshoulderX','RshoulderY','RshoulderZ'])
total_Xtrain = []
for i, row in enumerate(X_true):
    total_Xtrain.append([row[0], row[1], row[2]])
    #change lists to dataframe
    df_x_true.loc[i]=[
        pd.Series(row[0][0]), pd.Series(row[0][1]), pd.Series(row[0][2]),
        pd.Series(row[1][0]), pd.Series(row[1][1]), pd.Series(row[1][2]),
        pd.Series(row[2][0]), pd.Series(row[2][1]), pd.Series(row[2][2])
    ]
for i, row in enumerate(X_false):
    #total_Xtrain.append([row[0], row[1], row[2]])
    df_x_false.loc[i]=[
        pd.Series(row[0][0]), pd.Series(row[0][1]), pd.Series(row[0][2]),
        pd.Series(row[1][0]), pd.Series(row[1][1]), pd.Series(row[1][2]),
        pd.Series(row[2][0]), pd.Series(row[2][1]), pd.Series(row[2][2])
    ]


#I have a json file with shape of (84,9,699) and I want to make it (84,6291)
bodyparts = []
scetch = []
limited_data = []
min_samples_size = 605
for i, row in enumerate(X_true):
    sample_size = []
    sample = []
    bodyparts.append(len(row))
    for bodypart in row:
        for xyz in bodypart:
            sample_size.append(len(xyz[:min_samples_size]))
            sample.append(xyz[:min_samples_size])
    limited_data.append(sample)
    scetch.append(sample_size)

for i, row in enumerate(X_false):
    sample_size = []
    sample = []
    bodyparts.append(len(row))
    for bodypart in row:
        for xyz in bodypart:
            sample_size.append(len(xyz[:min_samples_size]))
            sample.append(xyz[:min_samples_size])
    limited_data.append(sample)
    scetch.append(sample_size)
print(len(X_true))
print(bodyparts)
print(scetch)

print('+++++++')
data_array = np.array(limited_data)

print(data_array.shape)

# Reshape the array from (84, 9, 699) to (84, 6291)
print(data_array.shape)
reshaped_data = data_array.reshape(168, 9 * min_samples_size)
print(reshaped_data.shape)


RwristY_true = df_x_true['RwristY']
RwristY_false = df_x_false['RwristY']
#concat two series to in the axis 0
RwristY_Xtrain = pd.concat([RwristY_true, RwristY_false], axis=0)
#every row in the datafram will become a sample in the 3D array
#
total_Xtrain = []

#RwristY_Ytrain = [1] * len(RwristY_true) + [0] * len(RwristY_false)
RwristY_Ytrain = np.concatenate((np.ones(len(RwristY_true)), np.zeros(len(RwristY_false))))
print(RwristY_Xtrain.shape)
print(RwristY_Xtrain[0].shape)


y_train = [1] * len(X_true) + [0] * len(X_false)
X_train = X_true + X_false
#cut the data to the minimum size
RwristY_Xtrain = [series[:min_samples_size] for series in RwristY_Xtrain]

print(len(RwristY_Xtrain))
print(RwristY_Xtrain[0].shape)

#fillna for missing values
RwristY_Xtrain = pd.DataFrame(RwristY_Xtrain).fillna(0).values
print(len(RwristY_Ytrain))

lengths = [len(X) for X in RwristY_Xtrain if X is not None]
uniques = np.unique(lengths)
print(uniques)


X_train, X_test, y_train, y_test = train_test_split(reshaped_data, RwristY_Ytrain, test_size=0.3, random_state=4)


model = make_pipeline(StandardScaler(), SVC(kernel='rbf'))
model.fit(X_train, y_train)
print(X_test[0])
print(model.predict([X_test[0]]))
print(X_test[1])
print(model.predict([X_test[1]]))

print(model.predict(X_test))
print(y_test)
print(model.score(X_test, y_test))
param_grid = {'svc__C': [0.1, 1, 10], 'svc__gamma': [1, 0.1, 0.01]}
grid = GridSearchCV(model, param_grid, cv=5)
grid.fit(RwristY_Xtrain, RwristY_Ytrain)

print(grid.best_params_)
print(grid.best_score_)


# New data sample (3x3x699) - example
np.random.seed(3)
new_sample = np.random.rand(1, 5445)  # Flattened new sample
new_sample = np.ones((1, 5445))

# Predict the class (True/False) for the new sample
new_prediction = model.predict(new_sample)
print("New prediction:", new_prediction)

#save the sklearn model
import joblib
joblib.dump(model, 'model.pkl')
#load the model
model2 = joblib.load('model.pkl')
print(X_test.shape)
print(model2.predict(X_test))