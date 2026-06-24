# emotion_model.py
# This file loads the pretrained AI model from HuggingFace and runs emotion detection.

from transformers import pipeline

# pipeline() is a HuggingFace function that loads a pretrained model in one line.
# "text-classification" means we want to classify text into categories (emotions).
# The model is already trained on thousands of sentences — we just USE it, no training needed.

def load_model():
    emotion_pipeline = pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        return_all_scores=False
    )
    return emotion_pipeline

def analyze_emotion(text, emotion_pipeline):
    # Takes user text and returns detected emotion + confidence score
    result = emotion_pipeline(text)[0]
    
    emotion = result['label']     # e.g. "joy"
    confidence = result['score']  # e.g. 0.95 = 95%
    
    return emotion, confidence
