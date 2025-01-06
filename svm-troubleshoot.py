from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
import numpy as np
import pandas as pd
#make a mock dataset with 168 samples of 699 features with first 84 samples as true and the rest as false

np.random.seed(0)

X_true = np.random.rand(84, 699)
X_false = np.random.rand(84, 699)

X_train = np.concatenate((X_true, X_false), axis=0)
print("X_train.shape",X_train.shape)
Y_train = [1] * len(X_true) + [0] * len(X_false)
print('len y_train',len(Y_train))


model = make_pipeline(StandardScaler(), SVC(kernel='rbf'))
model.fit(X_train, Y_train)
param_grid = {'svc__C': [0.1, 1, 10], 'svc__gamma': [1, 0.1, 0.01]}
grid = GridSearchCV(model, param_grid, cv=5)
grid.fit(X_train, Y_train)
print(grid.best_params_)
print(grid.best_score_)


# The error is due to the fact that the input data is not in the correct format. The input data should be a 2D array where each row represents a sample and each column represents a feature. In the original code, the input data is a list of lists, where each list represents a feature. To fix this, the input data should be converted to a 2D array using numpy. I have provided a mock dataset with the correct format to demonstrate the correct usage of the SVM model. The code should now run without any errors.
