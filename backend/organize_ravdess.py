import os
import shutil

# SOURCE: where your Actor_01 ... Actor_24 folders exist
SOURCE_DIR = "data/archive"

# TARGET: new clean dataset
TARGET_DIR = "data/ravdess"

# RAVDESS emotion mapping
emotion_map = {
    "01": "neutral",
    "02": "calm",
    "03": "happy",
    "04": "sad",
    "05": "angry",
    "06": "fearful",
    "07": "disgust",
    "08": "surprised"
}

# Create target emotion folders
os.makedirs(TARGET_DIR, exist_ok=True)
for emotion in emotion_map.values():
    os.makedirs(os.path.join(TARGET_DIR, emotion), exist_ok=True)

print("📂 Organizing RAVDESS dataset...")

# Traverse Actor folders
for actor_folder in os.listdir(SOURCE_DIR):
    actor_path = os.path.join(SOURCE_DIR, actor_folder)

    if not os.path.isdir(actor_path):
        continue

    for file in os.listdir(actor_path):
        if not file.endswith(".wav"):
            continue

        try:
            emotion_code = file.split("-")[2]
            emotion_name = emotion_map.get(emotion_code)

            if emotion_name:
                src_file = os.path.join(actor_path, file)
                dst_file = os.path.join(TARGET_DIR, emotion_name, file)
                shutil.copy(src_file, dst_file)

        except Exception as e:
            print("⚠️ Skipped:", file, e)

print("✅ Dataset organized successfully!")
