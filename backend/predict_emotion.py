import pickle
from extract_features import extract_mfcc

model = pickle.load(open("models/emotion_model.pkl", "rb"))

def predict_emotion(audio_file):
    features = extract_mfcc(audio_file)
    return model.predict([features])[0]
