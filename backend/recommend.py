import pandas as pd

df = pd.read_csv("data/spotify_tracks.csv")

def recommend_songs(emotion, language="Tamil", limit=5):
    mood_map = {
        "happy": (0.6, 1.0),
        "sad": (0.0, 0.4),
        "calm": (0.3, 0.6),
        "angry": (0.5, 0.9),
        "fearful": (0.2, 0.5),
        "neutral": (0.4, 0.6),
        "disgust": (0.2, 0.5),
        "surprised": (0.6, 1.0)
    }

    low, high = mood_map.get(emotion, (0.4, 0.6))

    filtered = df[
        (df["valence"] >= low) &
        (df["valence"] <= high) &
        (df["language"] == language)
    ].sort_values("popularity", ascending=False)

    return filtered.head(limit)[
        ["track_name", "artist_name", "album_name", "track_url"]
    ]
