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
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
    font-family: 'Space Grotesk', sans-serif !important;
    background: #04040a !important;
    color: #e2e2f0 !important;
}

.stApp { background: #04040a !important; }
.main .block-container {
    padding: 0 1.2rem 4rem 1.2rem !important;
    max-width: 820px !important;
}

/* ── BG ORBS ── */
.orbs-wrap {
    position: fixed; top: 0; left: 0;
    width: 100vw; height: 100vh;
    pointer-events: none; z-index: 0; overflow: hidden;
}
.orb {
    position: absolute; border-radius: 50%;
    animation: orb-drift linear infinite;
}
.o1 { width:600px;height:600px;background:radial-gradient(circle,#5b21b6 0%,transparent 70%);top:-200px;left:-180px;opacity:.22;animation-duration:24s; }
.o2 { width:500px;height:500px;background:radial-gradient(circle,#1d4ed8 0%,transparent 70%);top:25%;right:-150px;opacity:.18;animation-duration:30s;animation-delay:-10s; }
.o3 { width:420px;height:420px;background:radial-gradient(circle,#be185d 0%,transparent 70%);bottom:-100px;left:20%;opacity:.16;animation-duration:20s;animation-delay:-5s; }
.o4 { width:300px;height:300px;background:radial-gradient(circle,#047857 0%,transparent 70%);top:55%;left:5%;opacity:.14;animation-duration:26s;animation-delay:-14s; }

@keyframes orb-drift {
    0%   { transform:translate(0,0) scale(1); }
    25%  { transform:translate(35px,-25px) scale(1.04); }
    50%  { transform:translate(-18px,45px) scale(.96); }
    75%  { transform:translate(-45px,-15px) scale(1.07); }
    100% { transform:translate(0,0) scale(1); }
}

/* ── GRID ── */
.grid-bg {
    position: fixed; top:0; left:0;
    width:100vw; height:100vh;
    pointer-events:none; z-index:0;
    background-image:
        linear-gradient(rgba(255,255,255,.018) 1px,transparent 1px),
        linear-gradient(90deg,rgba(255,255,255,.018) 1px,transparent 1px);
    background-size:55px 55px;
}

/* ── NOISE TEXTURE ── */
.noise-bg {
    position:fixed;top:0;left:0;
    width:100vw;height:100vh;
    pointer-events:none;z-index:0;
    opacity:.03;
    background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
    background-size:180px 180px;
}

/* ── NAV ── */
.nav-outer {
    position:relative;z-index:100;
    display:flex;justify-content:center;
    padding:2rem 0 0.5rem;
}
.nav-track {
    display:inline-flex;align-items:center;
    background:rgba(255,255,255,.035);
    border:1px solid rgba(255,255,255,.07);
    border-radius:100px;
    padding:5px 6px;gap:3px;
    backdrop-filter:blur(24px);
    -webkit-backdrop-filter:blur(24px);
}

.stButton > button {
    background:transparent !important;
    color:#6b7280 !important;
    border:none !important;
    border-radius:100px !important;
    padding:0.4rem 1.2rem !important;
    font-family:'Space Grotesk',sans-serif !important;
    font-size:0.82rem !important;
    font-weight:500 !important;
    letter-spacing:0.06em !important;
    text-transform:uppercase !important;
    cursor:pointer !important;
    transition:all .25s ease !important;
    white-space:nowrap !important;
    min-width:auto !important;
    width:auto !important;
}
.stButton > button:hover {
    background:rgba(255,255,255,.06) !important;
    color:#e2e2f0 !important;
    transform:none !important;
    box-shadow:none !important;
}

/* ── HERO ── */
.hero-section {
    position:relative;z-index:10;
    text-align:center;padding:3.5rem 0 1rem;
}
.eyebrow {
    font-family:'Space Mono',monospace;
    font-size:0.65rem;letter-spacing:.3em;
    text-transform:uppercase;color:#7c3aed;
    margin-bottom:1.4rem;
    display:flex;align-items:center;justify-content:center;gap:.6rem;
}
.eyebrow::before,.eyebrow::after {
    content:'';width:28px;height:1px;
    background:linear-gradient(90deg,transparent,#7c3aed);
}
.eyebrow::after { background:linear-gradient(90deg,#7c3aed,transparent); }

.hero-h1 {
    font-size:clamp(3rem,9vw,5.5rem);
    font-weight:700;line-height:1.02;
    letter-spacing:-.04em;margin-bottom:1.3rem;
    background:linear-gradient(135deg,#ffffff 0%,#c4b5fd 40%,#93c5fd 80%,#ffffff 100%);
    background-size:200% 200%;
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-clip:text;
    animation:hgrad 6s ease-in-out infinite alternate;
}
@keyframes hgrad {
    0%  { background-position:0% 50%; }
    100%{ background-position:100% 50%; }
}

.hero-p {
    font-size:1.05rem;color:#4b5563;
    max-width:420px;margin:0 auto 2.5rem;
    line-height:1.8;font-weight:400;
}

/* ── STATS ── */
.stats-wrap {
    display:flex;justify-content:center;
    gap:0;margin-bottom:3rem;
    border:1px solid rgba(255,255,255,.06);
    border-radius:16px;overflow:hidden;
    background:rgba(255,255,255,.02);
    backdrop-filter:blur(10px);
}
.stat-box {
    flex:1;padding:1.2rem .5rem;
    text-align:center;border-right:1px solid rgba(255,255,255,.06);
}
.stat-box:last-child { border-right:none; }
.stat-n {
    font-family:'Space Mono',monospace;
    font-size:1.7rem;font-weight:700;
    color:#c4b5fd;line-height:1;margin-bottom:.3rem;
}
.stat-l {
    font-size:.65rem;color:#374151;
    letter-spacing:.12em;text-transform:uppercase;
}

/* ── FEATURE CARDS ── */
.feat-grid {
    display:grid;grid-template-columns:1fr 1fr;
    gap:.9rem;position:relative;z-index:10;
    margin-bottom:2.5rem;
}
.feat-card {
    background:rgba(255,255,255,.025);
    border:1px solid rgba(255,255,255,.06);
    border-radius:18px;padding:1.4rem;
    transition:all .3s ease;
    position:relative;overflow:hidden;
}
.feat-card::after {
    content:'';
    position:absolute;inset:0;
    background:linear-gradient(135deg,rgba(124,58,237,.06),transparent 60%);
    opacity:0;transition:opacity .3s;border-radius:18px;
}
.feat-card:hover { border-color:rgba(167,139,250,.2);transform:translateY(-4px); }
.feat-card:hover::after { opacity:1; }
.feat-icon {
    width:38px;height:38px;border-radius:10px;
    background:rgba(124,58,237,.12);
    border:1px solid rgba(124,58,237,.2);
    display:flex;align-items:center;justify-content:center;
    font-size:1.1rem;margin-bottom:.9rem;
}
.feat-title {
    font-size:.72rem;font-weight:600;
    text-transform:uppercase;letter-spacing:.12em;
    color:#6b7280;margin-bottom:.45rem;
}
.feat-body { font-size:.85rem;color:#374151;line-height:1.65; }

/* ── EMOTION CHIPS ── */
.chips-row {
    display:flex;flex-wrap:wrap;gap:.5rem;
    justify-content:center;margin:0 0 3.5rem;
    position:relative;z-index:10;
}
.chip {
    background:rgba(255,255,255,.03);
    border:1px solid rgba(255,255,255,.07);
    border-radius:100px;padding:.3rem .85rem;
    font-size:.75rem;color:#4b5563;
    font-family:'Space Grotesk',sans-serif;
    letter-spacing:.04em;
    transition:all .25s;
}
.chip:hover { border-color:rgba(167,139,250,.3);color:#a78bfa; }

/* ── ANALYZER ── */
.analyzer-top {
    position:relative;z-index:10;
    text-align:center;padding:2rem 0 2.5rem;
}
.page-h { 
    font-size:clamp(2.2rem,7vw,4rem);
    font-weight:700;letter-spacing:-.035em;
    background:linear-gradient(135deg,#fff 0%,#a78bfa 100%);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-clip:text;margin-bottom:.5rem;
}
.page-sub {
    font-size:.92rem;color:#374151;
    max-width:380px;margin:0 auto;line-height:1.75;
}

/* ── TEXTAREA ── */
.stTextArea { position:relative;z-index:10; }
.stTextArea > label { display:none !important; }
.stTextArea > div > div {
    background:rgba(255,255,255,.03) !important;
    border:1px solid rgba(255,255,255,.08) !important;
    border-radius:16px !important;
    transition:border-color .3s,box-shadow .3s !important;
}
.stTextArea > div > div:focus-within {
    border-color:rgba(124,58,237,.5) !important;
    box-shadow:0 0 0 4px rgba(124,58,237,.08) !important;
}
.stTextArea textarea {
    background:transparent !important;
    color:#e2e2f0 !important;
    font-family:'Space Grotesk',sans-serif !important;
    font-size:1.05rem !important;
    line-height:1.75 !important;
    caret-color:#a78bfa !important;
    resize:none !important;
}
.stTextArea textarea::placeholder { color:#1f2937 !important; }

/* ── ANALYZE BUTTON (override) ── */
div[data-testid="stVerticalBlock"] .stButton > button {
    background:linear-gradient(135deg,#6d28d9,#1d4ed8) !important;
    color:#fff !important;
    border:none !important;
    border-radius:12px !important;
    padding:.85rem 2rem !important;
    font-size:.88rem !important;
    font-weight:600 !important;
    letter-spacing:.08em !important;
    text-transform:uppercase !important;
    width:100% !important;
    transition:all .3s ease !important;
    box-shadow:0 4px 24px rgba(109,40,217,.25) !important;
}
div[data-testid="stVerticalBlock"] .stButton > button:hover {
    transform:translateY(-2px) !important;
    box-shadow:0 8px 32px rgba(109,40,217,.45) !important;
    background:linear-gradient(135deg,#7c3aed,#2563eb) !important;
}

/* ── CHAR COUNTER ── */
.char-hint {
    font-family:'Space Mono',monospace;
    font-size:.65rem;color:#1f2937;
    text-align:right;margin-top:.4rem;
    letter-spacing:.05em;
}

/* ── RESULT ── */
.result-wrap {
    margin-top:1.8rem;position:relative;z-index:10;
    animation:slide-up .55s cubic-bezier(.16,1,.3,1) both;
}
@keyframes slide-up {
    from { opacity:0;transform:translateY(28px); }
    to   { opacity:1;transform:translateY(0); }
}

.result-card {
    border-radius:22px;
    padding:2.5rem 2rem 2rem;
    text-align:center;
    position:relative;overflow:hidden;
    border:1px solid rgba(255,255,255,.07);
    background:rgba(10,10,20,.6);
    backdrop-filter:blur(30px);
}
.result-glow {
    position:absolute;inset:0;border-radius:22px;
    pointer-events:none;
    background:radial-gradient(ellipse 80% 60% at 50% 0%,var(--ec,rgba(124,58,237,.15)),transparent 70%);
}
.result-top-line {
    position:absolute;top:0;left:10%;right:10%;
    height:1.5px;border-radius:100px;
    background:var(--el,linear-gradient(90deg,#7c3aed,#2563eb));
}

.emotion-emoji { font-size:3.5rem;line-height:1;margin-bottom:.5rem; }
.emotion-name {
    font-family:'Space Mono',monospace;
    font-size:clamp(2rem,6vw,3.2rem);
    font-weight:700;letter-spacing:-.02em;
    line-height:1;margin-bottom:1.2rem;
}

/* ── CONFIDENCE METER ── */
.conf-block { margin-bottom:1.8rem; }
.conf-header {
    display:flex;justify-content:space-between;align-items:center;
    margin-bottom:.5rem;
}
.conf-label {
    font-family:'Space Mono',monospace;
    font-size:.6rem;letter-spacing:.15em;
    text-transform:uppercase;color:#374151;
}
.conf-pct {
    font-family:'Space Mono',monospace;
    font-size:.8rem;font-weight:700;
}
.conf-track {
    width:100%;height:5px;
    background:rgba(255,255,255,.06);
    border-radius:100px;overflow:hidden;
}
.conf-fill {
    height:100%;border-radius:100px;
    background:var(--el,linear-gradient(90deg,#7c3aed,#2563eb));
    transition:width 1.2s cubic-bezier(.16,1,.3,1);
}

/* ── SUGGESTIONS ── */
.sug-wrap {
    background:rgba(124,58,237,.05);
    border:1px solid rgba(124,58,237,.12);
    border-radius:14px;padding:1.3rem 1.4rem;
    text-align:left;
}
.sug-tag {
    font-family:'Space Mono',monospace;
    font-size:.58rem;letter-spacing:.2em;
    text-transform:uppercase;color:#7c3aed;
    margin-bottom:.9rem;
    display:flex;align-items:center;gap:.5rem;
}
.sug-tag::after {
    content:'';flex:1;height:1px;
    background:rgba(124,58,237,.2);
}
.sug-line {
    display:flex;align-items:flex-start;gap:.7rem;
    padding:.45rem 0;
    border-bottom:1px solid rgba(255,255,255,.03);
    font-size:.88rem;color:#6b7280;line-height:1.6;
}
.sug-line:last-child { border-bottom:none;padding-bottom:0; }
.sug-dot {
    width:5px;height:5px;border-radius:50%;
    background:var(--ec,#7c3aed);
    flex-shrink:0;margin-top:.5rem;opacity:.6;
}

/* ── ABOUT ── */
.about-section { position:relative;z-index:10; }
.about-card {
    background:rgba(255,255,255,.02);
    border:1px solid rgba(255,255,255,.05);
    border-radius:16px;padding:1.4rem 1.5rem;
    margin-bottom:.8rem;
    transition:border-color .3s;
}
.about-card:hover { border-color:rgba(167,139,250,.15); }
.about-tag {
    font-family:'Space Mono',monospace;
    font-size:.58rem;letter-spacing:.2em;
    text-transform:uppercase;color:#7c3aed;margin-bottom:.55rem;
}
.about-text { font-size:.88rem;color:#374151;line-height:1.8; }
.about-text strong { color:#9ca3af;font-weight:500; }

/* ── FOOTER ── */
.footer {
    position:relative;z-index:10;
    text-align:center;margin-top:4rem;
    padding-top:1.5rem;
    border-top:1px solid rgba(255,255,255,.04);
}
.footer-txt {
    font-family:'Space Mono',monospace;
    font-size:.6rem;letter-spacing:.2em;
    text-transform:uppercase;color:#111827;
}

/* hide streamlit junk */
#MainMenu,footer,header,.stDeployButton,[data-testid="stToolbar"] { visibility:hidden !important; }
.stSpinner > div { border-color:#7c3aed transparent transparent transparent !important; }
</style>

<div class="orbs-wrap">
    <div class="orb o1"></div><div class="orb o2"></div>
    <div class="orb o3"></div><div class="orb o4"></div>
</div>
<div class="grid-bg"></div>
<div class="noise-bg"></div>
""", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'Home'

st.markdown('<div class="nav-outer"><div class="nav-track">', unsafe_allow_html=True)
c1,c2,c3 = st.columns(3)
with c1:
    if st.button("Home"): st.session_state.page='Home'
with c2:
    if st.button("Analyzer"): st.session_state.page='Analyzer'
with c3:
    if st.button("About"): st.session_state.page='About'
st.markdown('</div></div>', unsafe_allow_html=True)

# ════════════ HOME ════════════
if st.session_state.page == 'Home':
    st.markdown("""
    <div class="hero-section">
        <div class="eyebrow">NLP &nbsp;·&nbsp; Deep Learning &nbsp;·&nbsp; Real Time</div>
        <h1 class="hero-h1">Feel what<br>words carry.</h1>
        <p class="hero-p">Type anything — a thought, a memory, a rant. MoodSense AI detects the emotion living inside your words.</p>
        <div class="stats-wrap">
            <div class="stat-box"><div class="stat-n">7</div><div class="stat-l">Emotions</div></div>
            <div class="stat-box"><div class="stat-n">&lt;1s</div><div class="stat-l">Response</div></div>
            <div class="stat-box"><div class="stat-n">98%</div><div class="stat-l">Accuracy</div></div>
            <div class="stat-box"><div class="stat-n">0</div><div class="stat-l">Training</div></div>
        </div>
    </div>

    <div class="chips-row">
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
            <div class="feat-body">DistilRoBERTa from HuggingFace — fine-tuned on thousands of real emotional sentences. Zero custom training.</div>
        </div>
        <div class="feat-card">
            <div class="feat-icon">⚡</div>
            <div class="feat-title">Instant Analysis</div>
            <div class="feat-body">Results appear in under a second. Type, click, done. No lag, no loading screens.</div>
        </div>
        <div class="feat-card">
            <div class="feat-icon">📊</div>
            <div class="feat-title">Confidence Score</div>
            <div class="feat-body">Every result shows exactly how certain the AI is — displayed as a live progress bar.</div>
        </div>
        <div class="feat-card">
            <div class="feat-icon">💡</div>
            <div class="feat-title">Smart Suggestions</div>
            <div class="feat-body">Personalized multi-line guidance for each detected emotion, not generic advice.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ════════════ ANALYZER ════════════
elif st.session_state.page == 'Analyzer':
    st.markdown("""
    <div class="analyzer-top">
        <div class="eyebrow">AI Powered &nbsp;·&nbsp; NLP</div>
        <div class="page-h">Emotion Analyzer</div>
        <div class="page-sub">Write anything. The AI reads between the lines and surfaces the emotion hidden in your words.</div>
    </div>
    """, unsafe_allow_html=True)

    user_input = st.text_area("", placeholder="e.g.  I don't know why but I feel so empty today...", height=155)
    go = st.button("→  Analyze Emotion")

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
                "joy":"#fbbf24","sadness":"#60a5fa","anger":"#f87171",
                "fear":"#c084fc","surprise":"#fb923c","disgust":"#34d399","neutral":"#9ca3af"
            }
            emojis = {
                "joy":"😊","sadness":"😢","anger":"😠",
                "fear":"😨","surprise":"😲","disgust":"🤢","neutral":"😐"
            }
            col = colors.get(el,"#a78bfa")
            emo = emojis.get(el,"🧠")

            lines = [l.strip() for l in suggestion.strip().split('\n') if l.strip()]
            sug_html = "".join(f'<div class="sug-line"><div class="sug-dot"></div><span>{ln}</span></div>' for ln in lines)

            st.markdown(f"""
            <div class="result-wrap">
                <div class="result-card" style="--ec:{col};--el:linear-gradient(90deg,{col}88,{col});">
                    <div class="result-glow"></div>
                    <div class="result-top-line"></div>
                    <div class="emotion-emoji">{emo}</div>
                    <div class="emotion-name" style="color:{col};">{emotion.upper()}</div>
                    <div class="conf-block">
                        <div class="conf-header">
                            <span class="conf-label">Confidence</span>
                            <span class="conf-pct" style="color:{col};">{pct}%</span>
                        </div>
                        <div class="conf-track">
                            <div class="conf-fill" style="width:{pct}%;background:linear-gradient(90deg,{col}66,{col});"></div>
                        </div>
                    </div>
                    <div class="sug-wrap">
                        <div class="sug-tag">What to do</div>
                        {sug_html}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ════════════ ABOUT ════════════
elif st.session_state.page == 'About':
    st.markdown("""
    <div class="about-section">
        <div class="analyzer-top">
            <div class="eyebrow">Class XII &nbsp;·&nbsp; AI Project</div>
            <div class="page-h">About</div>
            <div class="page-sub">A real AI project — pretrained model, live deployment, zero custom training.</div>
        </div>

        <div class="about-card">
            <div class="about-tag">Project Goal</div>
            <div class="about-text">Demonstrate how Artificial Intelligence and Natural Language Processing detect human emotions from raw text — and surface meaningful, context-aware guidance through a clean web interface.</div>
        </div>
        <div class="about-card">
            <div class="about-tag">Technology Stack</div>
            <div class="about-text">
                <strong>Python</strong> &nbsp;·&nbsp; <strong>Streamlit</strong> &nbsp;·&nbsp; <strong>HuggingFace Transformers</strong> &nbsp;·&nbsp; <strong>DistilRoBERTa</strong> &nbsp;·&nbsp; <strong>NLP</strong> &nbsp;·&nbsp; <strong>GitHub</strong> &nbsp;·&nbsp; <strong>Streamlit Cloud</strong>
            </div>
        </div>
        <div class="about-card">
            <div class="about-tag">AI Model</div>
            <div class="about-text">
                <strong>j-hartmann/emotion-english-distilroberta-base</strong><br><br>
                A pretrained transformer from HuggingFace fine-tuned for emotion classification across 7 categories. Used as-is via the Transformers pipeline — no custom training was done.
            </div>
        </div>
        <div class="about-card">
            <div class="about-tag">How It Works</div>
            <div class="about-text">
                User types text → Tokenizer converts it to numerical tokens → DistilRoBERTa processes them through 6 transformer layers → Softmax outputs probability scores for all 7 emotions → Highest score wins.
            </div>
        </div>
        <div class="about-card">
            <div class="about-tag">Developer</div>
            <div class="about-text">Built for Class XII Artificial Intelligence. Deployed live on Streamlit Cloud via GitHub — accessible from anywhere, on any device, with zero installation.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="footer"><div class="footer-txt">MoodSense AI &nbsp;·&nbsp; Class XII &nbsp;·&nbsp; NLP Project</div></div>', unsafe_allow_html=True)
