# fake_news_model.py
# This file loads a pretrained fake news detection model from HuggingFace

from transformers import pipeline

def load_fake_news_model():
    fake_news_pipeline = pipeline(
        "text-classification",
        model="mrm8488/bert-tiny-finetuned-fake-news-detection"
    )
    return fake_news_pipeline

def analyze_news(text, fake_news_pipeline):
    result = fake_news_pipeline(text, truncation=True, max_length=512)[0]
    
    # This model returns LABEL_0 = FAKE, LABEL_1 = REAL
    raw_label = result['label']
    confidence = result['score']
    
    if raw_label == "LABEL_1":
        label = "REAL"
    else:
        label = "FAKE"
    
    return label, confidence
