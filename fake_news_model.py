# fake_news_model.py
# Fake news detection using keyword-based analysis
# This approach is transparent, explainable, and works reliably for a Class 12 project

def load_fake_news_model():
    # No heavy model needed - we return None and use keyword logic instead
    return None

def analyze_news(text, model=None):
    fake_keywords = [
        "miracle", "shocking", "you won't believe", "secret", "they don't want you to know",
        "cure", "hoax", "conspiracy", "illuminati", "100% proven", "doctors hate",
        "click here", "share before deleted", "banned", "cover up", "exposed",
        "makes us horny", "overnight cure", "instant fix", "one weird trick",
        "big pharma", "government hiding", "aliens confirmed", "end of the world",
        "free iphone", "you have been selected", "earn money fast", "work from home guaranteed",
        "obama", "biden", "trump" , "modi" , "deepstate", "satanic", "satanist",
        "third eye", "reptilian", "flat earth", "vaccines cause", "5g causes",
        "mind control", "chemtrails", "new world order", "crisis actor"
    ]

    real_keywords = [
        "according to", "researchers found", "study shows", "scientists say",
        "published in", "confirmed by", "official statement", "government announces",
        "data shows", "evidence suggests", "experts say", "report says",
        "nasa", "who", "cdc", "bbc", "reuters", "associated press",
        "university", "journal", "peer reviewed", "statistics show"
    ]

    text_lower = text.lower()

    fake_score = sum(1 for word in fake_keywords if word in text_lower)
    real_score = sum(1 for word in real_keywords if word in text_lower)

    if fake_score > real_score:
        confidence = min(0.99, 0.70 + fake_score * 0.08)
        return "FAKE", confidence
    elif real_score > 0:
        confidence = min(0.99, 0.70 + real_score * 0.06)
        return "REAL", confidence
    else:
        # Neutral text - flag as needs verification
        return "FAKE", 0.55
