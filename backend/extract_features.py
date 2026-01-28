import librosa
import numpy as np

def extract_mfcc(file_path):
    y, sr = librosa.load(file_path, duration=10, offset=0.5)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfcc.T, axis=0)
