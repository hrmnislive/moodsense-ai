# suggestions.py
# This file contains helpful suggestion messages for each detected emotion.
# Think of it as a dictionary — emotion name is the KEY, suggestion is the VALUE.

suggestions = {
    "joy": "That's wonderful! Keep spreading positivity and enjoy the moment. 😊",
    "sadness": "It's okay to feel sad sometimes. Talk to someone you trust or take a walk outside. 💙",
    "anger": "Take a deep breath. Step away for a moment and give yourself time to cool down. 🧘",
    "fear": "It's okay to feel scared. Break the problem into small steps and tackle one at a time. 💪",
    "surprise": "Life is full of unexpected moments! Embrace it and stay adaptable. 🌟",
    "disgust": "It's okay to feel uncomfortable. Try to remove yourself from the situation calmly. 🍃",
    "neutral": "You seem calm and balanced. A great state to be productive and focused! ✅"
}

def get_suggestion(emotion):
    # This function takes an emotion string and returns the matching suggestion.
    # .lower() converts emotion to lowercase so "Joy" and "joy" both work.
    return suggestions.get(emotion.lower(), "Stay mindful and take care of yourself. 🌿")
