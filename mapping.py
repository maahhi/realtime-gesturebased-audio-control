import joblib
from preprocessing2 import preprocess_data
def use_model(sample,mode='test'):
    print("use_model")
    model2 = joblib.load('model.pkl')
    sample = preprocess_data(sample,mode)
    print('use_model_sample',sample)
    print(model2.predict([sample]))
    return model2.predict([sample])
