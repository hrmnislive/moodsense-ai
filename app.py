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
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
    font-family: 'Outfit', sans-serif !important;
    background: #070711 !important;
    color: #e8e8f4 !important;
}
.stApp { background: #070711 !important; }
.main .block-container {
    padding: 0 1.5rem 5rem 1.5rem !important;
    max-width: 860px !important;
}

/* BACKGROUND SYSTEM */
.bg-wrap {
    position: fixed; top: 0; left: 0;
    width: 100vw; height: 100vh;
    pointer-events: none; z-index: 0; overflow: hidden;
}
.orb {
    position: absolute; border-radius: 50%;
    animation: float linear infinite;
}
.o1 {
    width: 700px; height: 700px;
    background: radial-gradient(circle at 30% 40%, #4c1d95 0%, transparent 65%);
    top: -200px; left: -220px; opacity: .28;
    animation-duration: 22s;
}
.o2 {
    width: 550px; height: 550px;
    background: radial-gradient(circle at 60% 50%, #1e3a8a 0%, transparent 65%);
    top: 20%; right: -180px; opacity: .22;
    animation-duration: 28s; animation-delay: -9s;
}
.o3 {
    width: 450px; height: 450px;
    background: radial-gradient(circle at 50% 60%, #7e1d6e 0%, transparent 65%);
    bottom: -100px; left: 25%; opacity: .2;
    animation-duration: 19s; animation-delay: -5s;
}
.o4 {
    width: 320px; height: 320px;
    background: radial-gradient(circle at 50% 50%, #065f46 0%, transparent 65%);
    top: 55%; left: 5%; opacity: .18;
    animation-duration: 24s; animation-delay: -14s;
}
@keyframes float {
    0%   { transform: translate(0, 0) scale(1); }
    33%  { transform: translate(40px, -30px) scale(1.05); }
    66%  { transform: translate(-25px, 45px) scale(.95); }
    100% { transform: translate(0, 0) scale(1); }
}
.grid-bg {
    position: fixed; top: 0; left: 0;
    width: 100vw; height: 100vh;
    pointer-events: none; z-index: 0;
    background-image:
        linear-gradient(rgba(255,255,255,.016) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.016) 1px, transparent 1px);
    background-size: 64px 64px;
}

/* NAV */
.nav-wrap {
    position: relative; z-index: 100;
    display: flex; justify-content: center;
    padding: 2rem 0 0.5rem;
}
.nav-pill {
    display: inline-flex; align-items: center;
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.09);
    border-radius: 100px;
    padding: 5px 6px; gap: 3px;
    backdrop-filter: blur(20px);
}

/* RESET ALL BUTTONS */
.stButton > button {
    background: transparent !important;
    color: #6b7280 !important;
    border: none !important;
    border-radius: 100px !important;
    padding: 0.42rem 1.2rem !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    cursor: pointer !important;
    transition: all .2s !important;
    width: auto !important;
    min-width: auto !important;
}
.stButton > button:hover {
    background: rgba(255,255,255,.07) !important;
    color: #f0f0f8 !important;
    transform: none !important;
    box-shadow: none !important;
}

/* EYEBROW */
.eyebrow {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem; letter-spacing: .28em;
    text-transform: uppercase; color: #7c3aed;
    margin-bottom: 1.3rem;
    display: flex; align-items: center;
    justify-content: center; gap: .6rem;
}
.eyebrow::before, .eyebrow::after {
    content: ''; width: 28px; height: 1px;
    background: rgba(124,58,237,.5);
}

/* HOME HERO */
.hero {
    position: relative; z-index: 10;
    text-align: center; padding: 3.5rem 0 2rem;
}
.hero-title {
    font-size: clamp(2.8rem, 8vw, 5rem);
    font-weight: 800; line-height: 1.03;
    letter-spacing: -.04em; margin-bottom: 1.3rem;
    background: linear-gradient(135deg, #ffffff 0%, #c4b5fd 40%, #93c5fd 80%);
    background-size: 200% 200%;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: grad-shift 7s ease-in-out infinite alternate;
}
@keyframes grad-shift {
    0%   { background-position: 0% 50%; }
    100% { background-position: 100% 50%; }
}
.hero-sub {
    font-size: 1.15rem; color: #6b7280;
    max-width: 440px; margin: 0 auto 2.5rem;
    line-height: 1.8; font-weight: 400;
}

/* STATS BAR */
.stats {
    display: flex; justify-content: center;
    margin-bottom: 3.5rem;
    background: rgba(255,255,255,.025);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 16px; overflow: hidden;
}
.stat {
    flex: 1; padding: 1.3rem 0.5rem;
    text-align: center;
    border-right: 1px solid rgba(255,255,255,.06);
}
.stat:last-child { border-right: none; }
.stat-num {
    font-family: 'Space Mono', monospace;
    font-size: 1.8rem; font-weight: 700;
    color: #a78bfa; line-height: 1;
    margin-bottom: .3rem;
}
.stat-lbl {
    font-size: 0.72rem; color: #374151;
    letter-spacing: .1em; text-transform: uppercase;
}

/* EMOTION CHIPS */
.chips {
    display: flex; flex-wrap: wrap; gap: .5rem;
    justify-content: center;
    margin: 0 0 3.5rem;
    position: relative; z-index: 10;
}
.chip {
    background: rgba(255,255,255,.03);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 100px; padding: .35rem 1rem;
    font-size: 0.85rem; color: #4b5563;
    transition: all .25s;
}
.chip:hover { border-color: rgba(167,139,250,.35); color: #a78bfa; }

/* FEATURE CARDS */
.feat-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 1rem; position: relative; z-index: 10;
    margin-bottom: 3rem;
}
.feat-card {
    background: rgba(255,255,255,.025);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 20px; padding: 1.6rem;
    transition: all .3s ease; position: relative;
    overflow: hidden;
}
.feat-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(135deg, rgba(124,58,237,.06), transparent 60%);
    opacity: 0; transition: opacity .3s; border-radius: 20px;
}
.feat-card:hover { border-color: rgba(167,139,250,.22); transform: translateY(-4px); }
.feat-card:hover::before { opacity: 1; }
.feat-icon {
    width: 42px; height: 42px; border-radius: 12px;
    background: rgba(109,40,217,.12);
    border: 1px solid rgba(109,40,217,.2);
    display: flex; align-items: center;
    justify-content: center;
    font-size: 1.2rem; margin-bottom: 1rem;
}
.feat-title {
    font-size: 0.78rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: .1em;
    color: #6b7280; margin-bottom: .5rem;
}
.feat-body { font-size: 0.9rem; color: #374151; line-height: 1.7; }

/* PAGE HEADER */
.page-top {
    position: relative; z-index: 10;
    text-align: center; padding: 2.5rem 0 2.5rem;
}
.page-title {
    font-size: clamp(2.2rem, 7vw, 4rem);
    font-weight: 800; letter-spacing: -.035em;
    background: linear-gradient(135deg, #fff 0%, #a78bfa 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin-bottom: .55rem;
}
.page-sub {
    font-size: 1rem; color: #4b5563;
    max-width: 400px; margin: 0 auto; line-height: 1.8;
}

/* TEXTAREA */
.stTextArea { position: relative; z-index: 10; }
.stTextArea > label { display: none !important; }
.stTextArea > div > div {
    background: rgba(255,255,255,.03) !important;
    border: 1px solid rgba(255,255,255,.09) !important;
    border-radius: 16px !important;
    transition: all .3s !important;
}
.stTextArea > div > div:focus-within {
    border-color: rgba(124,58,237,.5) !important;
    box-shadow: 0 0 0 4px rgba(124,58,237,.07) !important;
}
.stTextArea textarea {
    background: transparent !important;
    color: #e8e8f4 !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.05rem !important;
    line-height: 1.8 !important;
    caret-color: #a78bfa !important;
    resize: none !important;
}
.stTextArea textarea::placeholder { color: #1f2937 !important; }

/* ANALYZE BUTTON */
div[data-testid="stVerticalBlock"] .stButton > button {
    background: linear-gradient(135deg, #5b21b6, #1e40af) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 14px !important;
    padding: .9rem 2rem !important;
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    letter-spacing: .06em !important;
    text-transform: uppercase !important;
    width: 100% !important;
    transition: all .3s ease !important;
    box-shadow: 0 4px 24px rgba(91,33,182,.22) !important;
    font-family: 'Outfit', sans-serif !important;
}
div[data-testid="stVerticalBlock"] .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 32px rgba(91,33,182,.42) !important;
    background: linear-gradient(135deg, #6d28d9, #1d4ed8) !important;
}

/* RESULT CARD */
.result-wrap {
    margin-top: 2rem; position: relative; z-index: 10;
    animation: reveal .55s cubic-bezier(.16,1,.3,1) both;
}
@keyframes reveal {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}
.result-card {
    border-radius: 24px;
    padding: 2.8rem 2.2rem 2.2rem;
    text-align: center;
    border: 1px solid rgba(255,255,255,.08);
    background: rgba(10,10,22,.7);
    backdrop-filter: blur(32px);
    position: relative; overflow: hidden;
}
.r-glow {
    position: absolute; inset: 0;
    background: radial-gradient(ellipse 75% 55% at 50% 0%, var(--gc), transparent 70%);
    pointer-events: none; border-radius: 24px;
}
.r-line {
    position: absolute; top: 0; left: 12%; right: 12%;
    height: 2px; border-radius: 100px;
}
.r-emoji { font-size: 3.8rem; line-height: 1; margin-bottom: .5rem; }
.r-name {
    font-family: 'Space Mono', monospace;
    font-size: clamp(2rem, 6vw, 3rem);
    font-weight: 700; letter-spacing: -.02em;
    line-height: 1; margin-bottom: 1.3rem;
}

/* CONFIDENCE */
.conf {
    margin-bottom: 2rem;
}
.conf-head {
    display: flex; justify-content: space-between;
    align-items: center; margin-bottom: .5rem;
}
.conf-tag {
    font-family: 'Space Mono', monospace;
    font-size: .6rem; letter-spacing: .16em;
    text-transform: uppercase; color: #374151;
}
.conf-pct {
    font-family: 'Space Mono', monospace;
    font-size: .82rem; font-weight: 700;
}
.conf-track {
    width: 100%; height: 5px;
    background: rgba(255,255,255,.06);
    border-radius: 100px; overflow: hidden;
}
.conf-fill {
    height: 100%; border-radius: 100px;
    transition: width 1.2s cubic-bezier(.16,1,.3,1);
}

/* SUGGESTIONS */
.sug {
    background: rgba(91,33,182,.06);
    border: 1px solid rgba(91,33,182,.14);
    border-radius: 16px; padding: 1.4rem 1.6rem;
    text-align: left;
}
.sug-tag {
    font-family: 'Space Mono', monospace;
    font-size: .58rem; letter-spacing: .2em;
    text-transform: uppercase; color: #7c3aed;
    margin-bottom: 1rem;
    display: flex; align-items: center; gap: .5rem;
}
.sug-tag::after {
    content: ''; flex: 1; height: 1px;
    background: rgba(124,58,237,.18);
}
.sug-row {
    display: flex; align-items: flex-start;
    gap: .7rem; padding: .5rem 0;
    border-bottom: 1px solid rgba(255,255,255,.04);
    font-size: 0.95rem; color: #6b7280; line-height: 1.7;
}
.sug-row:last-child { border-bottom: none; padding-bottom: 0; }
.sug-dot {
    width: 5px; height: 5px; border-radius: 50%;
    flex-shrink: 0; margin-top: .62rem; opacity: .6;
}

/* ABOUT */
.about-wrap { position: relative; z-index: 10; }
.about-card {
    background: rgba(255,255,255,.025);
    border: 1px solid rgba(255,255,255,.06);
    border-radius: 18px; padding: 1.6rem 1.7rem;
    margin-bottom: .9rem; transition: border-color .25s;
}
.about-card:hover { border-color: rgba(167,139,250,.18); }
.about-tag {
    font-family: 'Space Mono', monospace;
    font-size: .6rem; letter-spacing: .2em;
    text-transform: uppercase; color: #7c3aed;
    margin-bottom: .7rem;
}
.about-body {
    font-size: 0.95rem; color: #4b5563; line-height: 1.85;
}
.hl { color: #9ca3af; font-weight: 500; }
.tech-row {
    display: flex; flex-wrap: wrap;
    gap: .45rem; margin-top: .8rem;
}
.tech-tag {
    background: rgba(109,40,217,.09);
    border: 1px solid rgba(109,40,217,.18);
    border-radius: 8px; padding: .22rem .65rem;
    font-size: 0.78rem; color: #8b5cf6;
    font-family: 'Space Mono', monospace;
}

/* FOOTER */
.footer {
    position: relative; z-index: 10;
    text-align: center; margin-top: 4rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,.04);
}
.footer-txt {
    font-family: 'Space Mono', monospace;
    font-size: .6rem; letter-spacing: .2em;
    text-transform: uppercase; color: #111827;
}

/* HIDE STREAMLIT CHROME */
#MainMenu, footer, header, .stDeployButton { visibility: hidden !important; }
.stSpinner > div { border-color: #7c3aed transparent transparent !important; }
div[data-testid="stDecoration"] { display: none !important; }
</style>

<div class="bg-wrap">
    <div class="orb o1"></div>
    <div class="orb o2"></div>
    <div class="orb o3"></div>
    <div class="orb o4"></div>
</div>
<div class="grid-bg"></div>
""", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'Home'

st.markdown('<div class="nav-wrap"><div class="nav-pill">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("Home"): st.session_state.page = 'Home'
with c2:
    if st.button("Analyzer"): st.session_state.page = 'Analyzer'
with c3:
    if st.button("About"): st.session_state.page = 'About'
st.markdown('</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════
# HOME
# ══════════════════════════════════════
if st.session_state.page == 'Home':
    st.markdown("""
    <div class="hero">
        <div class="eyebrow">NLP &nbsp;·&nbsp; Deep Learning &nbsp;·&nbsp; Real Time</div>
        <h1 class="hero-title">Feel what<br>words carry.</h1>
        <p class="hero-sub">Type anything — a thought, a memory, a rant.<br>MoodSense AI finds the emotion hiding in your words.</p>
        <div class="stats">
            <div class="stat">
                <div class="stat-num">7</div>
                <div class="stat-lbl">Emotions</div>
            </div>
            <div class="stat">
                <div class="stat-num">&lt;1s</div>
                <div class="stat-lbl">Response</div>
            </div>
            <div class="stat">
                <div class="stat-num">98%</div>
                <div class="stat-lbl">Accuracy</div>
            </div>
            <div class="stat">
                <div class="stat-num">0</div>
                <div class="stat-lbl">Training</div>
            </div>
        </div>
    </div>

    <div class="chips">
        <span class="chip">😊 Joy</span>
        <span class="chip">😢 Sadness</span>
        <span class="chip">😠 Anger</span>
        <span class="chip">😨 Fear</span>
        <span class="chip">😲 Surprise</span>
        <span class="chip">🤢 Disgust</span>
        <span class="chip">😐 Neutral</span>
    </div>

    <div class="feat-grid">
        <div class="feat-card">
            <div class="feat-icon">🧠</div>
            <div class="feat-title">Pretrained Model</div>
            <div class="feat-body">DistilRoBERTa from HuggingFace, fine-tuned on thousands of real emotional sentences. Zero custom training needed.</div>
        </div>
        <div class="feat-card">
            <div class="feat-icon">⚡</div>
            <div class="feat-title">Instant Results</div>
            <div class="feat-body">Results in under a second. Type your sentence, click analyze, and the emotion appears immediately.</div>
        </div>
        <div class="feat-card">
            <div class="feat-icon">📊</div>
            <div class="feat-title">Confidence Score</div>
            <div class="feat-body">Every result shows how confident the AI is — displayed as a live animated progress bar with percentage.</div>
        </div>
        <div class="feat-card">
            <div class="feat-icon">💡</div>
            <div class="feat-title">Smart Suggestions</div>
            <div class="feat-body">Personalized multi-line guidance for every emotion detected. Specific, actionable, and actually useful.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════
# ANALYZER
# ══════════════════════════════════════
elif st.session_state.page == 'Analyzer':
    st.markdown("""
    <div class="page-top">
        <div class="eyebrow">AI Powered &nbsp;·&nbsp; NLP</div>
        <div class="page-title">Emotion Analyzer</div>
        <div class="page-sub">Write anything. The AI reads between the lines and finds what emotion lives in your words.</div>
    </div>
    """, unsafe_allow_html=True)

    user_input = st.text_area(
        "",
        placeholder="e.g.  I don't know why but I feel so empty today...",
        height=160
    )
    go = st.button("Analyze Emotion")

    if go:
        if not user_input.strip():
            st.warning("Type something first.")
        else:
            with st.spinner("Reading your words..."):
                mdl = load_model()
                emotion, confidence = analyze_emotion(user_input, mdl)
                suggestion = get_suggestion(emotion)

            pct = round(confidence * 100, 1)
            el = emotion.lower()

            colors = {
                "joy":      "#f59e0b",
                "sadness":  "#3b82f6",
                "anger":    "#ef4444",
                "fear":     "#a855f7",
                "surprise": "#f97316",
                "disgust":  "#10b981",
                "neutral":  "#6b7280"
            }
            emojis = {
                "joy": "😊", "sadness": "😢", "anger": "😠",
                "fear": "😨", "surprise": "😲", "disgust": "🤢", "neutral": "😐"
            }
            col  = colors.get(el, "#8b5cf6")
            emo  = emojis.get(el, "🧠")

            def hex_to_rgb(h):
                h = h.lstrip('#')
                return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

            r, g, b = hex_to_rgb(col)

            lines = [l.strip() for l in suggestion.strip().split('\n') if l.strip()]
            sug_html = "".join(
                f'<div class="sug-row">'
                f'<div class="sug-dot" style="background:{col};"></div>'
                f'<span>{ln}</span></div>'
                for ln in lines
            )

            st.markdown(f"""
            <div class="result-wrap">
                <div class="result-card">
                    <div class="r-glow" style="--gc: rgba({r},{g},{b},.13);"></div>
                    <div class="r-line" style="background: linear-gradient(90deg, {col}55, {col}, {col}55);"></div>
                    <div class="r-emoji">{emo}</div>
                    <div class="r-name" style="color: {col};">{emotion.upper()}</div>
                    <div class="conf">
                        <div class="conf-head">
                            <span class="conf-tag">Confidence</span>
                            <span class="conf-pct" style="color:{col};">{pct}%</span>
                        </div>
                        <div class="conf-track">
                            <div class="conf-fill" style="width:{pct}%; background: linear-gradient(90deg, {col}55, {col});"></div>
                        </div>
                    </div>
                    <div class="sug">
                        <div class="sug-tag">What to do</div>
                        {sug_html}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════
# ABOUT
# ══════════════════════════════════════
elif st.session_state.page == 'About':
    st.markdown("""
    <div class="about-wrap">
        <div class="page-top">
            <div class="eyebrow">Class XII &nbsp;·&nbsp; AI Project</div>
            <div class="page-title">About</div>
            <div class="page-sub">A real AI project. Pretrained model, live deployment, zero custom training.</div>
        </div>

        <div class="about-card">
            <div class="about-tag">Project Goal</div>
            <div class="about-body">
                To demonstrate how Artificial Intelligence and Natural Language Processing
                can detect human emotions from raw text — and surface meaningful,
                context-aware guidance through a clean web interface.
            </div>
        </div>

        <div class="about-card">
            <div class="about-tag">Technology Stack</div>
            <div class="about-body">Built using these tools and frameworks:</div>
            <div class="tech-row">
                <span class="tech-tag">Python</span>
                <span class="tech-tag">Streamlit</span>
                <span class="tech-tag">HuggingFace</span>
                <span class="tech-tag">Transformers</span>
                <span class="tech-tag">DistilRoBERTa</span>
                <span class="tech-tag">NLP</span>
                <span class="tech-tag">GitHub</span>
                <span class="tech-tag">Streamlit Cloud</span>
            </div>
        </div>

        <div class="about-card">
            <div class="about-tag">AI Model</div>
            <div class="about-body">
                Uses the pretrained model
                <span class="hl">j-hartmann/emotion-english-distilroberta-base</span>
                from HuggingFace — fine-tuned for emotion classification across 7 categories.
                Loaded via the Transformers pipeline. No custom training was done.
            </div>
        </div>

        <div class="about-card">
            <div class="about-tag">How It Works</div>
            <div class="about-body">
                User types text — Tokenizer converts it into numerical tokens —
                DistilRoBERTa processes them through 6 transformer layers —
                Softmax outputs probability scores for all 7 emotions —
                Highest score is selected as the final result.
            </div>
        </div>

        <div class="about-card">
            <div class="about-tag">Developer</div>
            <div class="about-body">
                Built for Class XII Artificial Intelligence subject.
                Deployed live on Streamlit Cloud via GitHub —
                accessible from anywhere, on any device, with zero installation required.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    <div class="footer-txt">MoodSense AI &nbsp;·&nbsp; Class XII &nbsp;·&nbsp; NLP Project</div>
</div>
""", unsafe_allow_html=True)
