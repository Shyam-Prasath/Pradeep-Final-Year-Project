from fastapi import FastAPI
import requests
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import xml.etree.ElementTree as ET

import pandas as pd
from pydantic import BaseModel
from record_audio import record_voice
from predict_emotion import predict_emotion
from recommend import recommend_songs

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def infer_emotion(row):
    valence = row["valence"]
    energy = row["energy"]

    if valence >= 0.6 and energy >= 0.6:
        return "Happy"
    elif valence <= 0.4 and energy <= 0.4:
        return "Sad"
    elif energy >= 0.75 and valence <= 0.5:
        return "Angry"
    elif energy <= 0.4 and valence >= 0.5:
        return "Calm"
    else:
        return "Neutral"
    


class VoiceRequest(BaseModel):
    language: str

@app.get("/latest-tamil-songs")
def latest_tamil_songs():
    url = "https://itunes.apple.com/search"
    params = {
        "term": "tamil",
        "media": "music",
        "entity": "song",
        "country": "IN",
        "limit": 20
    }
    response = requests.get(url, params=params)
    return response.json()


@app.get("/indian-songs")
def indian_songs():
    url = "https://itunes.apple.com/search"
    params = {
        "term": "india",
        "media": "music",
        "entity": "song",
        "country": "IN",
        "limit": 60   # fetch large pool once
    }
    return requests.get(url, params=params).json()


@app.get("/weekly-top-tamil")
def weekly_top_tamil():
    url = "https://itunes.apple.com/search"
    params = {
        "term": "Tamil",
        "media": "music",
        "entity": "song",
        "attribute": "genreIndex",
        "limit": 25
    }
    return requests.get(url, params=params).json()

@app.get("/new-tamil-hits")
def new_tamil_hits():
    url = "https://itunes.apple.com/search"
    params = {
        "term": "Tamil",
        "media": "music",
        "entity": "song",
        "limit": 100
    }

    data = requests.get(url, params=params).json()
    results = data.get("results", [])

    movie_songs = [
        song for song in results
        if "Motion Picture" in song.get("collectionName", "")
        or "Original Motion Picture" in song.get("collectionName", "")
    ]

    songs_2026 = [
        song for song in movie_songs
        if song.get("releaseDate", "").startswith("2026")
    ]

    final_songs = songs_2026 if songs_2026 else movie_songs[:10]

    return {
        "year": "2026" if songs_2026 else "latest",
        "resultCount": len(final_songs),
        "results": final_songs[:10]
    }


@app.get("/tamil-artists")
def tamil_artists():
    search_url = "https://itunes.apple.com/search"
    lookup_url = "https://itunes.apple.com/lookup"

    params = {
        "term": "Tamil",
        "media": "music",
        "entity": "musicArtist",
        "country": "IN",
        "limit": 50
    }

    artists = requests.get(search_url, params=params).json().get("results", [])

    enriched_artists = []
    seen = set()

    for artist in artists:
        artist_id = artist.get("artistId")
        artist_name = artist.get("artistName")

        if not artist_id or artist_name in seen:
            continue

        seen.add(artist_name)

        # 🔥 Lookup one song for image
        lookup_params = {
            "id": artist_id,
            "entity": "song",
            "limit": 1
        }

        songs = requests.get(lookup_url, params=lookup_params).json().get("results", [])

        image = None
        if len(songs) > 1:
            image = songs[1].get("artworkUrl100")

        enriched_artists.append({
            "artistName": artist_name,
            "artistId": artist_id,
            "image": image
        })

        if len(enriched_artists) >= 12:
            break

    return {"results": enriched_artists}


@app.get("/latest-songs")
def latest_songs():
    url = "https://itunes.apple.com/search"
    params = {
        "term": "tamil",
        "media": "music",
        "entity": "song",
        "country": "IN",
        "limit": 2000
    }
    response = requests.get(url, params=params)
    return response.json()



@app.get("/tamil-movie-songs")
def tamil_movie_songs():
    url = "https://itunes.apple.com/search"
    params = {
        "term": "Tamil",
        "media": "music",
        "entity": "song",
        "country": "IN",
        "limit": 200
    }

    data = requests.get(url, params=params).json()
    results = data.get("results", [])

    # ✅ FILTER: song title contains "Leo" (case-insensitive)
    leo_songs = [
        song for song in results
        if song.get("trackName")
        and "leo" in song["trackName"].lower()
        and song.get("previewUrl")
    ]

    return {
        "movie": "Leo",
        "songs": leo_songs
    }


@app.get("/tamil-latest-songs")
def tamil_latest_songs():
    url = "https://itunes.apple.com/search"
    params = {
        "term": "Tamil",
        "media": "music",
        "entity": "song",
        "country": "IN",
        "limit": 50
    }

    data = requests.get(url, params=params).json()
    results = data.get("results", [])

    playable = [s for s in results if s.get("previewUrl")]
    playable.sort(key=lambda x: x.get("releaseDate", ""), reverse=True)

    return {"songs": playable[:9]}


@app.get("/tamil-music-news")
def tamil_music_news(page: int = 1):
    rss_url = "https://news.google.com/rss/search?q=Tamil+music+songs&hl=en-IN&gl=IN&ceid=IN:en"
    res = requests.get(rss_url)
    root = ET.fromstring(res.content)

    items = list(root.iter("item"))

    PER_PAGE = 5
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE

    articles = []

    for item in items[start:end]:
        articles.append({
            "title": item.find("title").text,
            "link": item.find("link").text,
            "description": item.find("description").text,
            "pubDate": item.find("pubDate").text
        })

    return {
        "page": page,
        "articles": articles
    }

@app.post("/predict")
def predict(req: VoiceRequest):

    # 1️⃣ Record voice
    record_voice()

    # 2️⃣ Predict emotion
    emotion = predict_emotion("input.wav")

    # 3️⃣ Recommend songs
    songs_df = recommend_songs(emotion, req.language)

    # 4️⃣ Convert to JSON
    songs = []
    for _, row in songs_df.iterrows():
        songs.append({
            "track_name": row["track_name"],
            "artist_name": row["artist_name"],
            "track_url": row["track_url"]
        })

    return {
        "emotion": emotion,
        "songs": songs[:]
    }


@app.get("/analytics/summary")
def analytics_summary():
    df = pd.read_csv("data/spotify_tracks.csv")

    df["emotion"] = df.apply(infer_emotion, axis=1)

    return {
        "totalSongs": len(df),
        "totalArtists": df["artist_name"].nunique(),
        "languages": df["language"].value_counts().to_dict(),
        "emotions": df["emotion"].value_counts().to_dict(),
        "topArtists": (
            df["artist_name"]
            .value_counts()
            .head(5)
            .to_dict()
        )
    }


@app.get("/latest-language-songs")
def latest_language_songs(language: str = "Tamil"):
    url = "https://itunes.apple.com/search"

    params = {
        "term": language,
        "media": "music",
        "entity": "song",
        "country": "IN",
        "limit": 50
    }

    response = requests.get(url, params=params)
    return response.json()