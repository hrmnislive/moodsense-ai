import streamlit as st
from emotion_model import load_model, analyze_emotion
from suggestions import get_suggestion

st.set_page_config(
    page_title="MoodSense AI",
    page_icon="🧠",
    layout="centered"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0f0f0f;
        color: #f0f0f0;
    }
    .main { background-color: #0f0f0f; }
    .hero { text-align: center; padding: 3rem 0 2rem 0; }
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
    .confidence-text { font-size: 1rem; color: #888888; margin-bottom: 1.5rem; }
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
    .info-card p { font-size: 0.9rem; color: #888888; line-height: 1.6; margin: 0; }
    .joy { color: #FFD700; }
    .sadness { color: #6699FF; }
    .anger { color: #FF4444; }
    .fear { color: #AA66FF; }
    .surprise { color: #FF9900; }
    .disgust { color: #66CC66; }
    .neutral { color: #AAAAAA; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
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
    }
    .stButton > button:hover { opacity: 0.85; color: #000000; }
    .stTextArea textarea {
        background-color: #1a1a1a !important;
        color: #f0f0f0 !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 8px !important;
        font-size: 1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'Home'

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
            <div class="info-card">
                <h3>How It Works</h3>
                <p>You type any sentence. Our AI model reads it and identifies the dominant emotion using Natural Language Processing.</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class="info-card">
                <h3>Instant Results</h3>
                <p>Get your emotion detected in seconds along with a confidence score and a personalized suggestion.</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="info-card">
                <h3>7 Emotions Detected</h3>
                <p>Joy, Sadness, Anger, Fear, Surprise, Disgust, Neutral detected with high accuracy.</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class="info-card">
                <h3>Pretrained Model</h3>
                <p>Uses a HuggingFace DistilRoBERTa model trained on thousands of real-world emotional sentences.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align:center; color:#555555; font-size:0.85rem;">
            Click <strong style="color:#aaaaaa;">Analyzer</strong> above to get started
        </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == 'Analyzer':
    st.markdown("""
        <div class="hero">
            <h1>Analyze</h1>
            <p>Type anything. A thought, a sentence, how your day went. The AI will detect the emotion behind it.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    user_input = st.text_area(
        label="",
        placeholder="e.g. I am really stressed about my exams...",
        height=150
    )

    if st.button("Analyze Emotion"):
        if user_input.strip() == "":
            st.warning("Please enter some text first.")
        else:
            with st.spinner("Analyzing..."):
                model = load_model()
                emotion, confidence = analyze_emotion(user_input, model)
                suggestion = get_suggestion(emotion)

            confidence_percent = round(confidence * 100, 2)
            emotion_lower = emotion.lower()

            st.markdown(f"""
                <div class="result-card">
                    <div class="emotion-label {emotion_lower}">{emotion.upper()}</div>
                    <div class="confidence-text">Confidence: {confidence_percent}%</div>
                    <div class="suggestion-box">💡 {suggestion}</div>
                </div>
            """, unsafe_allow_html=True)

elif st.session_state.page == 'About':
    st.markdown("""
        <div class="hero">
            <h1>About</h1>
            <p>A Class 12 AI project demonstrating how machines understand human emotions through text.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
        <div class="info-card">
            <h3>Project Goal</h3>
            <p>To demonstrate how Artificial Intelligence and Natural Language Processing can identify human emotions from text input and provide meaningful, context-aware suggestions in real time.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="info-card">
            <h3>Technology Stack</h3>
            <p>Python, Streamlit, HuggingFace Transformers, DistilRoBERTa, NLP</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="info-card">
            <h3>AI Model</h3>
            <p>j-hartmann/emotion-english-distilroberta-base — a pretrained transformer model fine-tuned specifically for emotion classification across 7 categories.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="info-card">
            <h3>Developer</h3>
            <p>Built as an Artificial Intelligence project for Class XII. Demonstrates real-world application of NLP and deep learning without any custom model training.</p>
        </div>
    """, unsafe_allow_html=True)
