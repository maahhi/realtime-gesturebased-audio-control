#load dataframe
import pandas as pd
import numpy as np

df = pd.read_csv('data-700ish.csv')
df = df.dropna()

#make gestures to numbers
df['Gestures'] = df['Gestures'].apply(eval)
df['Gestures'] = df['Gestures'].apply(lambda x: list(x.keys())[0])
#map Closed_Fist to 0, Open_Palm to 1 and others to 2
df['Gestures'] = df['Gestures'].map({'Closed_Fist':0,'Open_Palm':1,'None':2,
                                     'Victory':2, 'Pointing_Up':2, 'Thumb_Down':2,'Thumb_Up':2})



X_train = np.zeros((df.shape[0],2*(df.shape[1]-2)))
Y_train = np.array(df['Gestures'])

#flatten the data and get rid of z axis
for i in range(0,df.shape[0]):
    for j,keyname in enumerate(df.columns[2:]):
        #str to dict
        position = eval(df[keyname].iloc[i])
        X_train[i][2 * j] = position['x']
        X_train[i][2 * j + 1] = position['y']




#standardize the data
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X_train)
scaled_data = scaler.transform(X_train)

#split the data
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.model_selection import train_test_split
X = scaled_data
y = df['Gestures']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)
print(len(X_train),len(X_test))
'''
#train the model
from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier(n_estimators=100)
rfc.fit(X_train, y_train)

#evaluate the model
predictions = rfc.predict(X_test)

#for i in range(len(predictions)):
#    print(predictions[i],y_test.iloc[i])

print(classification_report(y_test,predictions))
print(confusion_matrix(y_test,predictions))

from sklearn.ensemble import GradientBoostingClassifier
gbc = GradientBoostingClassifier(n_estimators=100)
gbc.fit(X_train, y_train)

predictions = gbc.predict(X_test)
print(classification_report(y_test,predictions))
print(confusion_matrix(y_test,predictions))
'''
#learn a mlp model
from sklearn.neural_network import MLPClassifier
mlp = MLPClassifier(hidden_layer_sizes=(30,30,30))
mlp.fit(X_train,y_train)

predictions = mlp.predict(X_test)
print(classification_report(y_test,predictions))
print(confusion_matrix(y_test,predictions))

# draw learning curve to see if the model is overfitting
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve
import matplotlib
matplotlib.use('Agg')
# Compute the learning curve
train_sizes, train_scores, test_scores = learning_curve(
    mlp, X_train, y_train, cv=5, train_sizes=np.linspace(0.1, 1.0, 10), scoring='accuracy'
)

# Calculate mean and standard deviation for training and test scores
train_scores_mean = np.mean(train_scores, axis=1)
train_scores_std = np.std(train_scores, axis=1)
test_scores_mean = np.mean(test_scores, axis=1)
test_scores_std = np.std(test_scores, axis=1)

# Plot learning curve
plt.figure(figsize=(10, 6))
plt.plot(train_sizes, train_scores_mean, label="Training score")
plt.plot(train_sizes, test_scores_mean, label="Cross-validation score")

# Fill the area around the mean curve to show standard deviation
plt.fill_between(train_sizes, train_scores_mean - train_scores_std, train_scores_mean + train_scores_std, alpha=0.1)
plt.fill_between(train_sizes, test_scores_mean - test_scores_std, test_scores_mean + test_scores_std, alpha=0.1)

plt.title("Learning Curve for MLP Classifier over media pipe")
plt.xlabel("Training Set Size")
plt.ylabel("Accuracy Score")
plt.legend(loc="best")
plt.grid()
plt.savefig("learning_curve.png")


#save the model
import joblib
joblib.dump(scaler, 'scaler.pkl')
joblib.dump(mlp, 'mlp.pkl')



