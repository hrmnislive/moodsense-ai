# fake_news_model.py
# This file loads a pretrained fake news detection model from HuggingFace

from transformers import pipeline

def load_fake_news_model():
    # This model is more balanced and accurate for fake news detection
    fake_news_pipeline = pipeline(
        "text-classification",
        model="GonzaloA/fake-news-detector"
    )
    return fake_news_pipeline

def analyze_news(text, fake_news_pipeline):
    # Takes news text and returns label (REAL/FAKE) and confidence score
    result = fake_news_pipeline(text, truncation=True, max_length=512)[0]
    label = result['label']      # "REAL" or "FAKE"
    confidence = result['score'] # e.g. 0.93 = 93%
    return label, confidence
