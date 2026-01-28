# 🎵 Kholi Music – AI-Powered Music Recommendation Platform

Kholi Music is a full-stack, AI-driven music recommendation web application that intelligently suggests songs based on language, popularity, emotion, and audio features.  
The platform combines a modern music UI, real-time APIs, and machine-learning–powered analytics to deliver a rich, interactive listening experience.

---

## 🚀 Features

### 🎧 Music Discovery
- Browse latest Tamil & Indian songs
- Alphabet-based album filtering (A–Z, 0–9)
- Live song preview playback
- Load-more pagination for albums

### 🌐 Language-Based Selection
- Filter songs by:
  - Tamil
  - Hindi
  - Telugu
  - Malayalam
  - English
- Real-time search with starts-with filtering

### 🤖 AI & Emotion Integration
- Emotion-based music recommendation system
- Voice emotion detection module
- Audio feature analysis (energy, valence, tempo, etc.)

### 📊 Analytics Dashboard
- Total songs, artists, languages & emotions
- Animated counters with + indicators
- Circular progress indicators
- Interactive charts using Chart.js
  - Songs per emotion
  - Language distribution
  - Top artists

### 🎶 Smart Player
- Modal-based music player
- Rotating disc animation
- Single global audio instance (prevents overlap)
- Preview availability handling

### 🎨 UI / UX Highlights
- Fully responsive (Bootstrap)
- Owl Carousel sliders
- WOW.js animations
- Clean dark-music theme
- Dynamic brand text switch:
  - “Madan Music” → “Kholi Music” after delay

---

## 🧠 Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript (ES6)
- Bootstrap
- jQuery
- Owl Carousel
- WOW.js
- Chart.js

### Backend (API)
- Python (FastAPI / Flask)
- iTunes public dataset
- Custom ML endpoints

### AI / ML
- Audio feature extraction
- Emotion classification
- Popularity & language filtering
---

## 🔗 API Endpoints Used

GET /latest-songs
GET /latest-tamil-songs
GET /indian-songs
GET /weekly-top-tamil
GET /new-tamil-hits
GET /tamil-artists
GET /analytics/summary
GET /latest-language-songs?language=Tamil

---

## 📂 Project Structure

```
/
├── index.html
├── albums-store.html
├── analytics.html
├── language-selection.html
├── audio.html
├── voice.html
├── emotion.html
├── style.css
├── js/
│ ├── plugins.js
│ ├── active.js
│ └── custom scripts
├── img/
│ └── bg-img/
└── README.md
```

---

## 🕒 Dynamic Branding Logic

- Header and footer initially display “Madan Music”
- Automatically switches to “Kholi Music” after a delay
- Implemented using class-based DOM selection to avoid duplicate IDs

---

## ▶️ How to Run

1. Start backend server:


uvicorn main:app --reload

2. Open `index.html` in browser
3. Ensure backend runs on:


http://127.0.0.1:8000


---

## 🧪 Tested On

- Google Chrome (recommended)
- Microsoft Edge
- Mozilla Firefox

---

## 📌 Current Features

- User authentication & playlists
- Spotify API integration
- Real-time voice recording
- Recommendation history
- Cloud deployment

## 📷 Live Preview

![WhatsApp Image 2026-01-25 at 7 31 45 PM](https://github.com/user-attachments/assets/5a75efd5-17fa-44ee-904e-71daa958d031)

---
## Model
![WhatsApp Image 2026-01-25 at 7 31 45 PM (1)](https://github.com/user-attachments/assets/768474bb-9794-41ae-a79e-dd03bb6f8e12)

---
## Solution 
![WhatsApp Image 2026-01-25 at 7 31 45 PM (2)](https://github.com/user-attachments/assets/9792fc21-bdc2-4ee0-b3ac-a49c4a054ec0)
