# emotion_model.py
# This file loads the pretrained AI model from HuggingFace and runs emotion detection.

from transformers import pipeline

# pipeline() is a HuggingFace function that loads a pretrained model in one line.
# "text-classification" means we want to classify text into categories (emotions).
# The model "j-hartmann/emotion-english-distilroberta-base" is already trained
# on thousands of sentences to detect 7 emotions. We don't train it — we just USE it.

@st.cache_resource
def load_model():
    emotion_pipeline = pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        return_all_scores=False  # Only return the TOP emotion, not all 7 scores
    )
    return emotion_pipeline

def analyze_emotion(text):
    # This function takes user input text and returns the detected emotion + confidence.
    emotion_pipeline = load_model()
    
    # The model returns a list like: [{'label': 'joy', 'score': 0.95}]
    result = emotion_pipeline(text)[0]
    
    emotion = result['label']       # The emotion name e.g. "joy"
    confidence = result['score']    # The confidence score e.g. 0.95 means 95%
    
    return emotion, confidence
