'''
This file takes the body gesture's csv files and creates an MLP model to classify them into 6 classes
0- No action
1- Left hand up
2- Right hand up
3- Both hands point to the left
4- Bothe hands point to the right
5- Both hands up
These actions are later mapped into a playback action that is determinded by MaxMSP, this plays the song.
'''


import pandas as pd
import numpy as np


if __name__ == '__name__':
    X_train = []
    Y_train = []
    classes = ['g0','g1','g2','g3', 'g4', 'g5']

    for i,c in enumerate(classes):
        df = pd.read_csv(c + '.csv')
        data_array = df.to_numpy()
        X_train.append(data_array)
        Y_train.append(np.ones(data_array.shape[0])*i)

    X_train = np.vstack(X_train)
    #standard scaler
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    Y_train = np.hstack(Y_train)
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

    print("class count:", mlp.classes_)

    #save mlp model
    import pickle
    filename = '_mlp_demo2.sav'
    pickle.dump(mlp, open(filename, 'wb'))

    #save standard scaler
    filename = '_scaler_demo2.sav'
    pickle.dump(scaler, open(filename, 'wb'))

    prediction = mlp.predict(X_train)
    print(y_train)
    print("---------------")
    print(prediction)

