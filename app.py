# app.py
# This is the MAIN file. It runs the entire Streamlit website.
# Streamlit reads this file and turns it into a working webpage.

import streamlit as st
from emotion_model import load_model, analyze_emotion
from suggestions import get_suggestion

# ─── PAGE CONFIG ───────────────────────────────────────────────
# This sets the browser tab title, icon, and layout of the webpage.
st.set_page_config(
    page_title="MoodSense AI",
    page_icon="🧠",
    layout="centered"
)

# ─── CUSTOM CSS STYLING ────────────────────────────────────────
# We inject custom CSS to make the website look professional and clean.
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0f0f0f;
        color: #f0f0f0;
    }

    .main {
        background-color: #0f0f0f;
    }

    /* Navigation bar styling */
    .nav-bar {
        display: flex;
        justify-content: center;
        gap: 2rem;
        padding: 1rem 0 2rem 0;
        border-bottom: 1px solid #2a2a2a;
        margin-bottom: 2rem;
    }

    .nav-btn {
        background: none;
        border: none;
        color: #aaaaaa;
        font-size: 0.95rem;
        cursor: pointer;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        font-weight: 500;
        padding: 0.3rem 0.8rem;
        border-radius: 4px;
        transition: all 0.2s;
    }

    .nav-btn:hover, .nav-btn.active {
        color: #ffffff;
        background-color: #1f1f1f;
    }

    /* Hero section */
    .hero {
        text-align: center;
        padding: 3rem 0 2rem 0;
    }

    .hero h1 {
        font-size: 3rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #ffffff 0%, #888888 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero p {
        font-size: 1.1rem;
        color: #888888;
        font-weight: 300;
        max-width: 500px;
        margin: 0 auto;
        line-height: 1.7;
    }

    /* Result card */
    .result-card {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 2rem;
        margin-top: 1.5rem;
        text-align: center;
    }

    .emotion-label {
        font-size: 2.5rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-bottom: 0.3rem;
    }

    .confidence-text {
        font-size: 1rem;
        color: #888888;
        margin-bottom: 1.5rem;
    }

    .suggestion-box {
        background: #111111;
        border-left: 3px solid #ffffff;
        border-radius: 6px;
        padding: 1rem 1.2rem;
        text-align: left;
        font-size: 0.95rem;
        color: #cccccc;
        line-height: 1.6;
    }

    /* About cards */
    .info-card {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .info-card h3 {
        font-size: 1rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .info-card p {
        font-size: 0.9rem;
        color: #888888;
        line-height: 1.6;
        margin: 0;
    }

    /* Emotion colors */
    .joy { color: #FFD700; }
    .sadness { color: #6699FF; }
    .anger { color: #FF4444; }
    .fear { color: #AA66FF; }
    .surprise { color: #FF9900; }
    .disgust { color: #66CC66; }
    .neutral { color: #AAAAAA; }

    /* Hide streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Analyze button */
    .stButton > button {
        width: 100%;
        background-color: #ffffff;
        color: #000000;
        border: none;
        padding: 0.75rem;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 8px;
        cursor: pointer;
        letter-spacing: 0.03em;
        transition: opacity 0.2s;
    }

    .stButton > button:hover {
        opacity: 0.85;
        color: #000000;
    }

    /* Text area */
    .stTextArea textarea {
        background-color: #1a1a1a !important;
        color: #f0f0f0 !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 8px !important;
        font-size: 1rem !important;
        font-family: 'Inter', sans-serif !important;
    }
    </style>
""", unsafe_allow_html=True)

# ─── SESSION STATE FOR NAVIGATION ──────────────────────────────
# st.session_state stores data between interactions.
# Here we use it to remember which page the user is on.
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# ─── NAVIGATION BAR ────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠  Home"):
        st.session_state.page = 'Home'
with col2:
    if st.button("🧠  Analyzer"):
        st.session_state.page = 'Analyzer'
with col3:
    if st.button("ℹ️  About"):
        st.session_state.page = 'About'

# ─── HOME PAGE ─────────────────────────────────────────────────
if st.session_state.page == 'Home':

    st.markdown("""
        <div class="hero">
            <h1>MoodSense AI</h1>
            <p>An intelligent emotion detection system powered by Natural Language Processing and pretrained deep learning models.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div
