# load dataframe
import pandas as pd
import numpy as np

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



pos_class_gesture = 'gesture_class_0'#'right_hand_up''M_openhands'
X_train = body_preprocessing(pos_class_gesture)
num_pos_class = X_train.shape[0]
neg_class_gestures = ['gesture_class_1','gesture_class_2','gesture_class_3', 'gesture_class_4', 'gesture_class_5']
#concatenate the negative class gestures
a = X_train.shape[0]
print('main class members',a)
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
Y_train = np.zeros(X_train.shape[0])
cls = 1
last_len = X_train.shape[0]
for neg_class_gesture in neg_class_gestures:
    X_train = np.concatenate((X_train, body_preprocessing(neg_class_gesture)), axis=0)
    Y_train = np.concatenate((Y_train, cls*np.ones(X_train.shape[0]-last_len)), axis=0)
    print('main class members', X_train.shape[0]-last_len)
    last_len = X_train.shape[0]
    cls += 1



"""
#randomley drop some of positive class and then some of negative class, but at the end i want balanced dataset
#drop 50% of positive class
subset_pos_class = 24
subset_neg_class = 24
#randomly select a subset from X_train with sebset_pos_class and subset_neg_class
#set the seed
np.random.seed(42)
pos_class_indices = np.random.choice(num_pos_class, subset_pos_class, replace=False)
neg_class_indices = np.random.choice(range(num_pos_class,X_train.shape[0]), subset_neg_class, replace=False)
#subset the data
X_train = np.concatenate((X_train[pos_class_indices],X_train[neg_class_indices]), axis=0)
Y_train = np.concatenate((Y_train[pos_class_indices],Y_train[neg_class_indices]), axis=0)

"""
#standard scaler
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)

print(X_train.shape)
print(Y_train.shape)

#split the data
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix
X_train, X_test, y_train, y_test = train_test_split(X_train, Y_train, test_size=0.3, random_state=45)


from sklearn.neural_network import MLPClassifier
mlp = MLPClassifier(hidden_layer_sizes=(30,30,30))
mlp.fit(X_train,y_train)

predictions = mlp.predict(X_test)
print(classification_report(y_test,predictions))
print(confusion_matrix(y_test,predictions))


from sklearn.ensemble import GradientBoostingClassifier
gbc = GradientBoostingClassifier(n_estimators=100)
gbc.fit(X_train, y_train)

predictions = gbc.predict(X_test)
print(classification_report(y_test,predictions))
print(confusion_matrix(y_test,predictions))

"""

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

plt.title("Learning Curve for Participant A Data")
plt.xlabel("Training Set Size")
plt.ylabel("Accuracy Score")
plt.legend(loc="best")
plt.grid()
plt.savefig("M-learningcurv.png")
"""
print("class count:", mlp.classes_)

#save mlp model
import pickle
filename = pos_class_gesture+'_mlp_demo2.sav'
pickle.dump(mlp, open(filename, 'wb'))

#save standard scaler
filename = pos_class_gesture + '_scaler_demo2.sav'
pickle.dump(scaler, open(filename, 'wb'))

prediction = mlp.predict(X_train)
print(y_train)
print("---------------")
print(prediction)

