import streamlit as st
from record_audio import record_voice
from predict_emotion import predict_emotion
from recommend import recommend_songs

st.set_page_config(page_title="Voice Based Song Recommendation")

st.title("🎵 Song Recommendation Based on Voice Tone")

language = st.selectbox(
    "Choose Language",
    ["Tamil", "Hindi", "Telugu", "Malayalam", "English"]
)

if st.button("🎤 Record Voice"):
    record_voice()
    emotion = predict_emotion("input.wav")

    st.success(f"Detected Emotion: {emotion.upper()}")

    st.subheader("🎶 Recommended Songs")
    songs = recommend_songs(emotion, language)

    for _, row in songs.iterrows():
        st.write(f"**{row['track_name']}** – {row['artist_name']}")
        st.write(row["track_url"])
