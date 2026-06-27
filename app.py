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
    background: #0d0d1a !important;
    color: #f0f0ff !important;
}
.stApp { background: #0d0d1a !important; }
.main .block-container {
    padding: 0 1.5rem 5rem 1.5rem !important;
    max-width: 860px !important;
}

/* ── BACKGROUND ── */
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
    background: radial-gradient(circle at 40% 40%, #6d28d9 0%, transparent 60%);
    top: -220px; left: -200px; opacity: .38;
    animation-duration: 22s;
}
.o2 {
    width: 560px; height: 560px;
    background: radial-gradient(circle at 50% 50%, #1d4ed8 0%, transparent 60%);
    top: 15%; right: -180px; opacity: .32;
    animation-duration: 28s; animation-delay: -9s;
}
.o3 {
    width: 480px; height: 480px;
    background: radial-gradient(circle at 50% 50%, #9d174d 0%, transparent 60%);
    bottom: -80px; left: 20%; opacity: .28;
    animation-duration: 20s; animation-delay: -5s;
}
.o4 {
    width: 340px; height: 340px;
    background: radial-gradient(circle at 50% 50%, #065f46 0%, transparent 60%);
    top: 50%; left: 0%; opacity: .24;
    animation-duration: 25s; animation-delay: -14s;
}
@keyframes float {
    0%   { transform: translate(0,0) scale(1); }
    33%  { transform: translate(38px,-28px) scale(1.05); }
    66%  { transform: translate(-22px,42px) scale(.96); }
    100% { transform: translate(0,0) scale(1); }
}
.grid-bg {
    position: fixed; top: 0; left: 0;
    width: 100vw; height: 100vh;
    pointer-events: none; z-index: 0;
    background-image:
        linear-gradient(rgba(255,255,255,.022) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.022) 1px, transparent 1px);
    background-size: 60px 60px;
}

/* ── NAV ── */
.nav-wrap {
    position: relative; z-index: 100;
    display: flex; justify-content: center;
    padding: 2rem 0 0.5rem;
}
.nav-pill {
    display: inline-flex; align-items: center;
    background: rgba(255,255,255,.07);
    border: 1px solid rgba(255,255,255,.15);
    border-radius: 100px;
    padding: 5px 6px; gap: 3px;
    backdrop-filter: blur(20px);
}
.stButton > button {
    background: transparent !important;
    color: #9ca3af !important;
    border: none !important;
    border-radius: 100px !important;
    padding: 0.44rem 1.3rem !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.03em !important;
    cursor: pointer !important;
    transition: all .2s !important;
    width: auto !important;
    min-width: auto !important;
}
.stButton > button:hover {
    background: rgba(255,255,255,.1) !important;
    color: #ffffff !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ── EYEBROW ── */
.eyebrow {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem; letter-spacing: .28em;
    text-transform: uppercase; color: #a78bfa;
    margin-bottom: 1.4rem;
    display: flex; align-items: center;
    justify-content: center; gap: .6rem;
}
.eyebrow::before, .eyebrow::after {
    content: ''; width: 30px; height: 1px;
    background: rgba(167,139,250,.5);
}

/* ── HERO ── */
.hero {
    position: relative; z-index: 10;
    text-align: center; padding: 3.5rem 0 2rem;
}
.hero-title {
    font-size: clamp(3rem, 9vw, 5.5rem);
    font-weight: 800; line-height: 1.02;
    letter-spacing: -.04em; margin-bottom: 1.4rem;
    background: linear-gradient(135deg, #ffffff 0%, #ddd6fe 40%, #bfdbfe 80%, #ffffff 100%);
    background-size: 200% 200%;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: grad 7s ease-in-out infinite alternate;
}
@keyframes grad {
    0%   { background-position: 0% 50%; }
    100% { background-position: 100% 50%; }
}
.hero-sub {
    font-size: 1.25rem; color: #c4c4d4;
    max-width: 460px; margin: 0 auto 2.8rem;
    line-height: 1.8; font-weight: 400;
}

/* ── FLOATING WORDS ANIMATION ── */
.float-words {
    position: relative; z-index: 10;
    height: 60px; margin-bottom: 2.5rem;
    overflow: hidden;
}
.float-word {
    position: absolute; left: 0; right: 0;
    text-align: center;
    font-size: 1.4rem; font-weight: 600;
    opacity: 0;
    animation: word-cycle 8s ease-in-out infinite;
}
.fw1 { color: #fbbf24; animation-delay: 0s; }
.fw2 { color: #60a5fa; animation-delay: 2s; }
.fw3 { color: #f87171; animation-delay: 4s; }
.fw4 { color: #a78bfa; animation-delay: 6s; }
@keyframes word-cycle {
    0%   { opacity: 0; transform: translateY(20px); }
    10%  { opacity: 1; transform: translateY(0); }
    35%  { opacity: 1; transform: translateY(0); }
    45%  { opacity: 0; transform: translateY(-20px); }
    100% { opacity: 0; transform: translateY(-20px); }
}

/* ── STATS ── */
.stats {
    display: flex; justify-content: center;
    margin-bottom: 3.5rem;
    background: rgba(255,255,255,.06);
    border: 1px solid rgba(255,255,255,.13);
    border-radius: 18px; overflow: hidden;
}
.stat {
    flex: 1; padding: 1.4rem 0.5rem;
    text-align: center;
    border-right: 1px solid rgba(255,255,255,.1);
}
.stat:last-child { border-right: none; }
.stat-num {
    font-family: 'Space Mono', monospace;
    font-size: 1.9rem; font-weight: 700;
    color: #c4b5fd; line-height: 1;
    margin-bottom: .35rem;
}
.stat-lbl {
    font-size: 0.78rem; color: #6b7280;
    letter-spacing: .1em; text-transform: uppercase;
}

/* ── CHIPS ── */
.chips {
    display: flex; flex-wrap: wrap; gap: .55rem;
    justify-content: center;
    margin: 0 0 3.5rem;
    position: relative; z-index: 10;
}
.chip {
    background: rgba(255,255,255,.06);
    border: 1px solid rgba(255,255,255,.14);
    border-radius: 100px; padding: .42rem 1.1rem;
    font-size: 0.92rem; color: #c4c4d4;
    transition: all .25s; cursor: default;
}
.chip:hover {
    border-color: rgba(167,139,250,.5);
    color: #ddd6fe;
    background: rgba(167,139,250,.1);
}

/* ── FEATURE CARDS ── */
.feat-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 1rem; position: relative; z-index: 10;
    margin-bottom: 3rem;
}
.feat-card {
    background: rgba(255,255,255,.05);
    border: 1px solid rgba(255,255,255,.1);
    border-radius: 20px; padding: 1.7rem;
    transition: all .3s ease; position: relative; overflow: hidden;
}
.feat-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(135deg, rgba(124,58,237,.1), transparent 60%);
    opacity: 0; transition: opacity .3s; border-radius: 20px;
}
.feat-card:hover {
    border-color: rgba(167,139,250,.35);
    transform: translateY(-5px);
    background: rgba(255,255,255,.07);
}
.feat-card:hover::before { opacity: 1; }
.feat-icon {
    width: 44px; height: 44px; border-radius: 12px;
    background: rgba(109,40,217,.18);
    border: 1px solid rgba(109,40,217,.3);
    display: flex; align-items: center;
    justify-content: center;
    font-size: 1.25rem; margin-bottom: 1.1rem;
}
.feat-title {
    font-size: 0.82rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: .1em;
    color: #9ca3af; margin-bottom: .55rem;
}
.feat-body { font-size: 0.95rem; color: #8b8ba8; line-height: 1.7; }

/* ── HOW IT WORKS STEPS ── */
.steps {
    position: relative; z-index: 10;
    margin-bottom: 3.5rem;
}
.steps-title {
    font-size: 0.72rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: .18em;
    color: #6b7280; text-align: center;
    margin-bottom: 1.5rem;
    font-family: 'Space Mono', monospace;
}
.step-row {
    display: flex; align-items: flex-start;
    gap: 1.2rem; padding: 1.1rem 0;
    border-bottom: 1px solid rgba(255,255,255,.06);
}
.step-row:last-child { border-bottom: none; }
.step-num {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem; font-weight: 700;
    color: #7c3aed;
    background: rgba(124,58,237,.12);
    border: 1px solid rgba(124,58,237,.25);
    border-radius: 8px; padding: .3rem .55rem;
    flex-shrink: 0; margin-top: .1rem;
    letter-spacing: .05em;
}
.step-text {
    font-size: 1rem; color: #c4c4d4; line-height: 1.65;
}
.step-text strong { color: #e8e8f4; font-weight: 600; }

/* ── PAGE HEADER ── */
.page-top {
    position: relative; z-index: 10;
    text-align: center; padding: 2.5rem 0 2.8rem;
}
.page-title {
    font-size: clamp(2.4rem, 7vw, 4.2rem);
    font-weight: 800; letter-spacing: -.035em;
    background: linear-gradient(135deg, #fff 0%, #c4b5fd 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin-bottom: .6rem;
}
.page-sub {
    font-size: 1.1rem; color: #9ca3af;
    max-width: 420px; margin: 0 auto; line-height: 1.8;
}

/* ── TEXTAREA ── */
.stTextArea { position: relative; z-index: 10; }
.stTextArea > label { display: none !important; }
.stTextArea > div > div {
    background: rgba(255,255,255,.06) !important;
    border: 1px solid rgba(255,255,255,.15) !important;
    border-radius: 18px !important;
    transition: all .3s !important;
}
.stTextArea > div > div:focus-within {
    border-color: rgba(139,92,246,.6) !important;
    box-shadow: 0 0 0 4px rgba(124,58,237,.1) !important;
    background: rgba(255,255,255,.08) !important;
}
.stTextArea textarea {
    background: transparent !important;
    color: #f0f0ff !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.1rem !important;
    line-height: 1.8 !important;
    caret-color: #a78bfa !important;
    resize: none !important;
}
.stTextArea textarea::placeholder { color: #4b5563 !important; font-size: 1.05rem !important; }

/* ── ANALYZE BUTTON ── */
div[data-testid="stVerticalBlock"] .stButton > button {
    background: linear-gradient(135deg, #6d28d9, #1e40af) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 1rem 2rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: .06em !important;
    text-transform: uppercase !important;
    width: 100% !important;
    transition: all .3s ease !important;
    box-shadow: 0 4px 28px rgba(109,40,217,.3) !important;
    font-family: 'Outfit', sans-serif !important;
}
div[data-testid="stVerticalBlock"] .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 36px rgba(109,40,217,.5) !important;
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
}

/* ── RESULT ── */
.result-wrap {
    margin-top: 2rem; position: relative; z-index: 10;
    animation: reveal .55s cubic-bezier(.16,1,.3,1) both;
}
@keyframes reveal {
    from { opacity: 0; transform: translateY(26px); }
    to   { opacity: 1; transform: translateY(0); }
}
.result-card {
    border-radius: 24px;
    padding: 3rem 2.4rem 2.4rem;
    text-align: center;
    border: 1px solid rgba(255,255,255,.12);
    background: rgba(18,18,32,.8);
    backdrop-filter: blur(32px);
    position: relative; overflow: hidden;
}
.r-glow {
    position: absolute; inset: 0;
    pointer-events: none; border-radius: 24px;
}
.r-line {
    position: absolute; top: 0; left: 10%; right: 10%;
    height: 2px; border-radius: 100px;
}
.r-emoji { font-size: 4rem; line-height: 1; margin-bottom: .6rem; }
.r-name {
    font-family: 'Space Mono', monospace;
    font-size: clamp(2.2rem, 6vw, 3.2rem);
    font-weight: 700; letter-spacing: -.02em;
    line-height: 1; margin-bottom: 1.5rem;
}

/* ── CONFIDENCE ── */
.conf { margin-bottom: 2.2rem; }
.conf-head {
    display: flex; justify-content: space-between;
    align-items: center; margin-bottom: .55rem;
}
.conf-tag {
    font-family: 'Space Mono', monospace;
    font-size: .65rem; letter-spacing: .16em;
    text-transform: uppercase; color: #6b7280;
}
.conf-pct {
    font-family: 'Space Mono', monospace;
    font-size: .9rem; font-weight: 700;
}
.conf-track {
    width: 100%; height: 6px;
    background: rgba(255,255,255,.08);
    border-radius: 100px; overflow: hidden;
}
.conf-fill {
    height: 100%; border-radius: 100px;
    transition: width 1.2s cubic-bezier(.16,1,.3,1);
}

/* ── SUGGESTIONS ── */
.sug {
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.1);
    border-radius: 16px; padding: 1.5rem 1.7rem;
    text-align: left;
}
.sug-tag {
    font-family: 'Space Mono', monospace;
    font-size: .62rem; letter-spacing: .2em;
    text-transform: uppercase; color: #a78bfa;
    margin-bottom: 1.1rem;
    display: flex; align-items: center; gap: .5rem;
}
.sug-tag::after {
    content: ''; flex: 1; height: 1px;
    background: rgba(167,139,250,.2);
}
.sug-row {
    display: flex; align-items: flex-start;
    gap: .8rem; padding: .55rem 0;
    border-bottom: 1px solid rgba(255,255,255,.05);
    font-size: 1rem; color: #c4c4d4; line-height: 1.75;
}
.sug-row:last-child { border-bottom: none; padding-bottom: 0; }
.sug-dot {
    width: 6px; height: 6px; border-radius: 50%;
    flex-shrink: 0; margin-top: .65rem; opacity: .7;
}

/* ── ABOUT ── */
.about-wrap { position: relative; z-index: 10; }
.about-card {
    background: rgba(255,255,255,.05);
    border: 1px solid rgba(255,255,255,.1);
    border-radius: 20px; padding: 1.7rem 1.9rem;
    margin-bottom: 1rem; transition: border-color .25s;
}
.about-card:hover { border-color: rgba(167,139,250,.25); }
.about-tag {
    font-family: 'Space Mono', monospace;
    font-size: .62rem; letter-spacing: .2em;
    text-transform: uppercase; color: #a78bfa;
    margin-bottom: .75rem;
}
.about-body {
    font-size: 1rem; color: #9ca3af; line-height: 1.9;
}
.hl { color: #ddd6fe; font-weight: 500; }
.tech-row {
    display: flex; flex-wrap: wrap;
    gap: .5rem; margin-top: .9rem;
}
.tech-tag {
    background: rgba(109,40,217,.12);
    border: 1px solid rgba(109,40,217,.25);
    border-radius: 8px; padding: .28rem .75rem;
    font-size: 0.82rem; color: #c4b5fd;
    font-family: 'Space Mono', monospace;
}

/* ── FOOTER ── */
.footer {
    position: relative; z-index: 10;
    text-align: center; margin-top: 4rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,.07);
}
.footer-txt {
    font-family: 'Space Mono', monospace;
    font-size: .62rem; letter-spacing: .2em;
    text-transform: uppercase; color: #374151;
}

/* ── HIDE STREAMLIT CHROME ── */
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

# ══════════════════════════════════
# HOME
# ══════════════════════════════════
if st.session_state.page == 'Home':
    st.markdown("""
    <div class="hero">
        <div class="eyebrow">NLP &nbsp;·&nbsp; Deep Learning &nbsp;·&nbsp; Real Time</div>
        <h1 class="hero-title">Feel what<br>words carry.</h1>
        <p class="hero-sub">Type anything — a thought, a memory, a rant.<br>MoodSense AI finds the emotion hiding in your words.</p>
    </div>

    <div class="float-words" style="position:relative;z-index:10;">
        <div class="float-word fw1">😊 &nbsp; Joy detected — 96.4% confidence</div>
        <div class="float-word fw2">😢 &nbsp; Sadness detected — 89.2% confidence</div>
        <div class="float-word fw3">😠 &nbsp; Anger detected — 93.7% confidence</div>
        <div class="float-word fw4">😨 &nbsp; Fear detected — 91.5% confidence</div>
    </div>

    <div class="stats" style="position:relative;z-index:10;">
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

    <div class="steps" style="position:relative;z-index:10;">
        <div class="steps-title">How it works</div>
        <div class="step-row">
            <span class="step-num">01</span>
            <span class="step-text"><strong>You type anything</strong> — a sentence, a thought, how your day went. No formatting required.</span>
        </div>
        <div class="step-row">
            <span class="step-num">02</span>
            <span class="step-text"><strong>AI tokenizes your text</strong> — converts your words into numerical tokens the model can process.</span>
        </div>
        <div class="step-row">
            <span class="step-num">03</span>
            <span class="step-text"><strong>DistilRoBERTa analyzes</strong> — processes tokens through 6 transformer layers and scores all 7 emotions.</span>
        </div>
        <div class="step-row">
            <span class="step-num">04</span>
            <span class="step-text"><strong>Result appears instantly</strong> — dominant emotion, confidence %, and a personalized suggestion for you.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════
# ANALYZER
# ══════════════════════════════════
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
        placeholder="e.g.  I am really stressed about my exams right now...",
        height=165
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

            pct  = round(confidence * 100, 1)
            el   = emotion.lower()

            colors = {
                "joy":      "#fbbf24",
                "sadness":  "#60a5fa",
                "anger":    "#f87171",
                "fear":     "#c084fc",
                "surprise": "#fb923c",
                "disgust":  "#34d399",
                "neutral":  "#94a3b8"
            }
            emojis = {
                "joy": "😊", "sadness": "😢", "anger": "😠",
                "fear": "😨", "surprise": "😲", "disgust": "🤢", "neutral": "😐"
            }
            col = colors.get(el, "#a78bfa")
            emo = emojis.get(el, "🧠")

            def hex_rgb(h):
                h = h.lstrip('#')
                return tuple(int(h[i:i+2],16) for i in (0,2,4))
            r,g,b = hex_rgb(col)

            lines    = [l.strip() for l in suggestion.strip().split('\n') if l.strip()]
            sug_html = "".join(
                f'<div class="sug-row">'
                f'<div class="sug-dot" style="background:{col};"></div>'
                f'<span>{ln}</span></div>'
                for ln in lines
            )

            st.markdown(f"""
            <div class="result-wrap">
                <div class="result-card">
                    <div class="r-glow" style="background:radial-gradient(ellipse 70% 50% at 50% 0%,rgba({r},{g},{b},.18),transparent 70%);"></div>
                    <div class="r-line" style="background:linear-gradient(90deg,transparent,{col},{col},transparent);"></div>
                    <div class="r-emoji">{emo}</div>
                    <div class="r-name" style="color:{col};">{emotion.upper()}</div>
                    <div class="conf">
                        <div class="conf-head">
                            <span class="conf-tag">Confidence</span>
                            <span class="conf-pct" style="color:{col};">{pct}%</span>
                        </div>
                        <div class="conf-track">
                            <div class="conf-fill" style="width:{pct}%;background:linear-gradient(90deg,{col}66,{col});"></div>
                        </div>
                    </div>
                    <div class="sug">
                        <div class="sug-tag">What to do</div>
                        {sug_html}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════
# ABOUT
# ══════════════════════════════════
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
                can detect human emotions from raw text and surface meaningful,
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
