import os
import pickle
from extract_features import extract_mfcc
from sklearn.svm import SVC

DATASET_PATH = "data/ravdess"

X = []
y = []

print("Scanning dataset...")

for emotion in os.listdir(DATASET_PATH):
    emotion_folder = os.path.join(DATASET_PATH, emotion)

    if not os.path.isdir(emotion_folder):
        continue

    print(f"Processing emotion: {emotion}")

    for file in os.listdir(emotion_folder):
        if file.endswith(".wav"):
            file_path = os.path.join(emotion_folder, file)
            try:
                features = extract_mfcc(file_path)
                X.append(features)
                y.append(emotion)
            except Exception as e:
                print("Error processing:", file_path)

print("Training model...")

model = SVC(kernel="linear", probability=True)
model.fit(X, y)

os.makedirs("models", exist_ok=True)
pickle.dump(model, open("models/emotion_model.pkl", "wb"))

print("Model trained successfully with ALL emotions!")
print("✅ Model saved to models/emotion_model.pkl")