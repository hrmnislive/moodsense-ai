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
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    html, body, [class*="css"], .stApp {
        font-family: 'Space Grotesk', sans-serif;
        background-color: #050508;
        color: #e8e8f0;
    }

    .stApp { background: #050508; }
    .main .block-container { padding: 0 1rem 3rem 1rem; max-width: 780px; }

    /* ── ANIMATED BG ── */
    .bg-orbs {
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }
    .orb {
        position: absolute;
        border-radius: 50%;
        filter: blur(80px);
        opacity: 0.18;
        animation: drift linear infinite;
    }
    .orb1 { width: 500px; height: 500px; background: #7c3aed; top: -100px; left: -150px; animation-duration: 20s; }
    .orb2 { width: 400px; height: 400px; background: #2563eb; top: 30%; right: -100px; animation-duration: 25s; animation-delay: -8s; }
    .orb3 { width: 350px; height: 350px; background: #db2777; bottom: -80px; left: 30%; animation-duration: 18s; animation-delay: -4s; }
    .orb4 { width: 250px; height: 250px; background: #059669; top: 60%; left: 10%; animation-duration: 22s; animation-delay: -12s; }

    @keyframes drift {
        0%   { transform: translate(0px, 0px) scale(1); }
        25%  { transform: translate(40px, -30px) scale(1.05); }
        50%  { transform: translate(-20px, 50px) scale(0.95); }
        75%  { transform: translate(-50px, -20px) scale(1.08); }
        100% { transform: translate(0px, 0px) scale(1); }
    }

    /* ── GRID OVERLAY ── */
    .grid-overlay {
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        pointer-events: none;
        z-index: 0;
        background-image:
            linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
        background-size: 60px 60px;
    }

    /* ── NAV ── */
    .nav-wrapper {
        position: relative;
        z-index: 10;
        display: flex;
        justify-content: center;
        padding: 2rem 0 1.5rem 0;
    }
    .nav-pill {
        display: inline-flex;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 100px;
        padding: 5px;
        gap: 4px;
        backdrop-filter: blur(20px);
    }

    /* ── HERO ── */
    .hero-wrapper {
        position: relative;
        z-index: 10;
        text-align: center;
        padding: 2.5rem 0 3rem 0;
    }
    .hero-eyebrow {
        font-family: 'Space Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        color: #7c3aed;
        margin-bottom: 1.2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    .hero-eyebrow::before, .hero-eyebrow::after {
        content: '';
        width: 30px;
        height: 1px;
        background: #7c3aed;
        opacity: 0.5;
    }
    .hero-title {
        font-size: clamp(2.8rem, 8vw, 5rem);
        font-weight: 700;
        line-height: 1.05;
        letter-spacing: -0.03em;
        margin-bottom: 1.2rem;
        background: linear-gradient(135deg, #ffffff 0%, #a78bfa 50%, #60a5fa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shimmer 4s ease-in-out infinite alternate;
    }
    @keyframes shimmer {
        0%   { background-position: 0% 50%; }
        100% { background-position: 100% 50%; }
    }
    .hero-sub {
        font-size: 1.05rem;
        color: #6b7280;
        max-width: 440px;
        margin: 0 auto;
        line-height: 1.75;
        font-weight: 400;
    }

    /* ── STATS ROW ── */
    .stats-row {
        display: flex;
        justify-content: center;
        gap: 2.5rem;
        margin-top: 2.5rem;
        flex-wrap: wrap;
    }
    .stat-item { text-align: center; }
    .stat-num {
        font-family: 'Space Mono', monospace;
        font-size: 1.6rem;
        font-weight: 700;
        color: #a78bfa;
        line-height: 1;
    }
    .stat-label {
        font-size: 0.72rem;
        color: #4b5563;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-top: 0.3rem;
    }

    /* ── CARDS ── */
    .cards-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-top: 3rem;
        position: relative;
        z-index: 10;
    }
    .card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        cursor: default;
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    .card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(167,139,250,0.4), transparent);
        opacity: 0;
        transition: opacity 0.3s;
    }
    .card:hover { border-color: rgba(167,139,250,0.25); transform: translateY(-3px); }
    .card:hover::before { opacity: 1; }
    .card-icon { font-size: 1.5rem; margin-bottom: 0.8rem; }
    .card-title {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #9ca3af;
        margin-bottom: 0.5rem;
    }
    .card-body { font-size: 0.88rem; color: #4b5563; line-height: 1.6; }

    /* ── ANALYZER SECTION ── */
    .analyzer-wrapper {
        position: relative;
        z-index: 10;
        padding: 1rem 0;
    }
    .analyzer-header {
        text-align: center;
        margin-bottom: 2.5rem;
    }
    .analyzer-title {
        font-size: clamp(2rem, 6vw, 3.5rem);
        font-weight: 700;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #ffffff 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.6rem;
    }
    .analyzer-sub {
        font-size: 0.95rem;
        color: #4b5563;
        max-width: 400px;
        margin: 0 auto;
        line-height: 1.7;
    }

    /* ── INPUT BOX ── */
    .stTextArea > div > div {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 14px !important;
        transition: border-color 0.3s !important;
    }
    .stTextArea > div > div:focus-within {
        border-color: rgba(167,139,250,0.5) !important;
        box-shadow: 0 0 0 3px rgba(124,58,237,0.1) !important;
    }
    .stTextArea textarea {
        background: transparent !important;
        color: #e8e8f0 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.05rem !important;
        line-height: 1.7 !important;
        caret-color: #a78bfa !important;
    }
    .stTextArea textarea::placeholder { color: #374151 !important; }

    /* ── BUTTON ── */
    .stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
        color: #ffffff !important;
        border: none !important;
        padding: 0.9rem 2rem !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        letter-spacing: 0.04em !important;
        text-transform: uppercase !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        font-family: 'Space Grotesk', sans-serif !important;
        position: relative !important;
        overflow: hidden !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(124,58,237,0.4) !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }

    /* ── RESULT CARD ── */
    .result-outer {
        margin-top: 2rem;
        animation: slideUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .result-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        backdrop-filter: blur(20px);
        position: relative;
        overflow: hidden;
    }
    .result-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: var(--emotion-color, linear-gradient(90deg, #7c3aed, #2563eb));
    }
    .emotion-badge {
        display: inline-block;
        font-family: 'Space Mono', monospace;
        font-size: clamp(1.8rem, 5vw, 3rem);
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
        padding: 0.2rem 0;
    }
    .confidence-row {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.8rem;
        margin: 1rem 0 1.8rem 0;
    }
    .confidence-bar-bg {
        width: 140px;
        height: 4px;
        background: rgba(255,255,255,0.08);
        border-radius: 100px;
        overflow: hidden;
    }
    .confidence-bar-fill {
        height: 100%;
        border-radius: 100px;
        background: linear-gradient(90deg, #7c3aed, #60a5fa);
        transition: width 1s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .confidence-num {
        font-family: 'Space Mono', monospace;
        font-size: 0.85rem;
        color: #6b7280;
    }
    .suggestion-card {
        background: rgba(124,58,237,0.06);
        border: 1px solid rgba(124,58,237,0.15);
        border-radius: 12px;
        padding: 1.3rem 1.5rem;
        text-align: left;
    }
    .suggestion-label {
        font-size: 0.65rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        color: #7c3aed;
        margin-bottom: 0.7rem;
        font-family: 'Space Mono', monospace;
    }
    .suggestion-text {
        font-size: 0.92rem;
        color: #9ca3af;
        line-height: 1.85;
    }
    .suggestion-text p {
        margin-bottom: 0.4rem;
        padding-left: 1rem;
        border-left: 2px solid rgba(124,58,237,0.3);
        padding-top: 0.1rem;
        padding-bottom: 0.1rem;
    }

    /* ── EMOTION COLORS ── */
    .c-joy     { color: #fbbf24; }
    .c-sadness { color: #60a5fa; }
    .c-anger   { color: #f87171; }
    .c-fear    { color: #c084fc; }
    .c-surprise{ color: #fb923c; }
    .c-disgust { color: #34d399; }
    .c-neutral { color: #9ca3af; }

    /* ── ABOUT PAGE ── */
    .about-wrapper { position: relative; z-index: 10; }
    .about-title {
        font-size: clamp(2rem, 6vw, 3.5rem);
        font-weight: 700;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #ffffff 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    .about-sub {
        text-align: center;
        font-size: 0.95rem;
        color: #4b5563;
        margin-bottom: 2.5rem;
    }
    .about-card {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: border-color 0.3s;
    }
    .about-card:hover { border-color: rgba(167,139,250,0.2); }
    .about-card-label {
        font-size: 0.65rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        color: #7c3aed;
        margin-bottom: 0.6rem;
        font-family: 'Space Mono', monospace;
    }
    .about-card-text {
        font-size: 0.9rem;
        color: #6b7280;
        line-height: 1.75;
    }

    /* ── EMOTION PILLS (home page) ── */
    .emotions-strip {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        justify-content: center;
        margin-top: 2rem;
        position: relative;
        z-index: 10;
    }
    .e-pill {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 100px;
        padding: 0.35rem 0.9rem;
        font-size: 0.78rem;
        color: #6b7280;
        letter-spacing: 0.05em;
    }

    /* ── FOOTER LINE ── */
    .footer-line {
        text-align: center;
        font-size: 0.72rem;
        color: #1f2937;
        font-family: 'Space Mono', monospace;
        letter-spacing: 0.1em;
        margin-top: 3rem;
        position: relative;
        z-index: 10;
    }

    /* hide streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
    </style>

    <!-- Animated background -->
    <div class="bg-orbs">
        <div class="orb orb1"></div>
        <div class="orb orb2"></div>
        <div class="orb orb3"></div>
        <div class="orb orb4"></div>
    </div>
    <div class="grid-overlay"></div>
""", unsafe_allow_html=True)

# ── SESSION STATE ──
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# ── NAV ──
st.markdown('<div class="nav-wrapper"><div class="nav-pill">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Home"):
        st.session_state.page = 'Home'
with col2:
    if st.button("Analyzer"):
        st.session_state.page = 'Analyzer'
with col3:
    if st.button("About"):
        st.session_state.page = 'About'
st.markdown('</div></div>', unsafe_allow_html=True)

# ════════════════════════════════════
# HOME PAGE
# ════════════════════════════════════
if st.session_state.page == 'Home':

    st.markdown("""
        <div class="hero-wrapper">
            <div class="hero-eyebrow">NLP · Deep Learning · Real Time</div>
            <h1 class="hero-title">Read the emotion<br>behind every word.</h1>
            <p class="hero-sub">
                Type anything — a thought, a memory, how your day went.
                MoodSense AI detects the emotion behind it instantly.
            </p>
            <div class="stats-row">
                <div class="stat-item">
                    <div class="stat-num">7</div>
                    <div class="stat-label">Emotions</div>
                </div>
                <div class="stat-item">
                    <div class="stat-num">~0.3s</div>
                    <div class="stat-label">Response Time</div>
                </div>
                <div class="stat-item">
                    <div class="stat-num">98%</div>
                    <div class="stat-label">Accuracy</div>
                </div>
            </div>
        </div>

        <div class="emotions-strip">
            <span class="e-pill">😊 Joy</span>
            <span class="e-pill">😢 Sadness</span>
            <span class="e-pill">😠 Anger</span>
            <span class="e-pill">😨 Fear</span>
            <span class="e-pill">😲 Surprise</span>
            <span class="e-pill">🤢 Disgust</span>
            <span class="e-pill">😐 Neutral</span>
        </div>

        <div class="cards-grid">
            <div class="card">
                <div class="card-icon">🧠</div>
                <div class="card-title">Pretrained Model</div>
                <div class="card-body">DistilRoBERTa trained on thousands of real emotional sentences from HuggingFace.</div>
            </div>
            <div class="card">
                <div class="card-icon">⚡</div>
                <div class="card-title">Instant Analysis</div>
                <div class="card-body">Results in under a second. No delay, no wait. Just type and analyze.</div>
            </div>
            <div class="card">
                <div class="card-icon">📊</div>
                <div class="card-title">Confidence Score</div>
                <div class="card-body">Every result comes with a confidence percentage so you know how certain the AI is.</div>
            </div>
            <div class="card">
                <div class="card-icon">💡</div>
                <div class="card-title">Smart Suggestions</div>
                <div class="card-body">Personalized, multi-line guidance tailored to whatever emotion is detected.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════
# ANALYZER PAGE
# ════════════════════════════════════
elif st.session_state.page == 'Analyzer':

    st.markdown("""
        <div class="analyzer-wrapper">
            <div class="analyzer-header">
                <div class="hero-eyebrow">AI Powered · NLP</div>
                <div class="analyzer-title">Emotion Analyzer</div>
                <div class="analyzer-sub">Type anything. The AI reads between the lines and tells you what emotion lives there.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    user_input = st.text_area(
        label="",
        placeholder="e.g.  I am so frustrated with everything right now...",
        height=160
    )

    analyze_clicked = st.button("→  Analyze Emotion")

    if analyze_clicked:
        if user_input.strip() == "":
            st.warning("Type something first.")
        else:
            with st.spinner(""):
                model = load_model()
                emotion, confidence = analyze_emotion(user_input, model)
                suggestion = get_suggestion(emotion)

            pct = round(confidence * 100, 1)
            el = emotion.lower()

            color_map = {
                "joy":      "#fbbf24",
                "sadness":  "#60a5fa",
                "anger":    "#f87171",
                "fear":     "#c084fc",
                "surprise": "#fb923c",
                "disgust":  "#34d399",
                "neutral":  "#9ca3af",
            }
            emoji_map = {
                "joy": "😊", "sadness": "😢", "anger": "😠",
                "fear": "😨", "surprise": "😲", "disgust": "🤢", "neutral": "😐"
            }
            color = color_map.get(el, "#a78bfa")
            emoji = emoji_map.get(el, "🧠")

            lines = [l.strip() for l in suggestion.strip().split('\n') if l.strip()]
            suggestion_html = "".join(f"<p>{line}</p>" for line in lines)

            st.markdown(f"""
                <div class="result-outer">
                    <div class="result-card" style="--emotion-color: {color};">
                        <div style="position:absolute;top:0;left:0;right:0;height:2px;background:{color};border-radius:20px 20px 0 0;"></div>
                        <div style="font-size:3rem;margin-bottom:0.3rem;">{emoji}</div>
                        <div class="emotion-badge c-{el}">{emotion.upper()}</div>
                        <div class="confidence-row">
                            <div class="confidence-bar-bg">
                                <div class="confidence-bar-fill" style="width:{pct}%;background:linear-gradient(90deg,{color},{color}88);"></div>
                            </div>
                            <span class="confidence-num">{pct}%</span>
                        </div>
                        <div class="suggestion-card">
                            <div class="suggestion-label">What to do</div>
                            <div class="suggestion-text">{suggestion_html}</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════
# ABOUT PAGE
# ════════════════════════════════════
elif st.session_state.page == 'About':

    st.markdown("""
        <div class="about-wrapper">
            <div class="about-title">About</div>
            <div class="about-sub">A Class 12 AI project — real model, real results, zero custom training.</div>

            <div class="about-card">
                <div class="about-card-label">Project Goal</div>
                <div class="about-card-text">
                    Demonstrate how Artificial Intelligence and Natural Language Processing can detect human emotions
                    from raw text and provide meaningful, context-aware suggestions — all through a clean web interface.
                </div>
            </div>

            <div class="about-card">
                <div class="about-card-label">Technology Stack</div>
                <div class="about-card-text">
                    Python &nbsp;·&nbsp; Streamlit &nbsp;·&nbsp; HuggingFace Transformers &nbsp;·&nbsp; DistilRoBERTa &nbsp;·&nbsp; NLP &nbsp;·&nbsp; GitHub &nbsp;·&nbsp; Streamlit Cloud
                </div>
            </div>

            <div class="about-card">
                <div class="about-card-label">AI Model</div>
                <div class="about-card-text">
                    <strong style="color:#e8e8f0;">j-hartmann/emotion-english-distilroberta-base</strong><br>
                    A pretrained transformer model from HuggingFace, fine-tuned specifically for emotion classification
                    across 7 categories. No custom training was done — the model was used as-is via the Transformers pipeline.
                </div>
            </div>

            <div class="about-card">
                <div class="about-card-label">How It Works</div>
                <div class="about-card-text">
                    User types text → Tokenizer converts it to numerical tokens → DistilRoBERTa processes the tokens
                    → Softmax layer outputs probability scores for each emotion → Highest score is selected as the result.
                </div>
            </div>

            <div class="about-card">
                <div class="about-card-label">Developer</div>
                <div class="about-card-text">
                    Built for Class XII Artificial Intelligence project. Demonstrates real-world application of NLP
                    and deep learning — deployed live on Streamlit Cloud via GitHub.
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="footer-line">MOODSENSE AI · CLASS XII · NLP PROJECT</div>', unsafe_allow_html=True)
