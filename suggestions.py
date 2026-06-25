# suggestions.py
# Contains detailed, multi-line suggestions for each detected emotion.

suggestions = {
    "joy": """You're radiating positive energy right now — that's powerful.
Use this moment to connect with someone you care about.
Channel this happiness into something creative or productive.
Celebrate small wins. You deserve to feel this good. 😊""",

    "sadness": """It's okay to feel sad — emotions are valid, not weaknesses.
Try talking to a friend or someone you trust about how you feel.
Step outside for a few minutes, fresh air genuinely helps.
Be kind to yourself today. Healing takes time, and that's okay. 💙""",

    "anger": """Take a slow, deep breath before reacting to anything.
Step away from the situation for a few minutes to reset.
Try writing down what made you angry — it helps release tension.
Remember: responding calmly is always stronger than reacting with anger. 🧘""",

    "fear": """Fear is just your brain trying to protect you — acknowledge it.
Break whatever is scaring you into the smallest possible steps.
Talk to someone you trust about what you are going through.
Courage is not the absence of fear — it is moving forward despite it. 💪""",

    "surprise": """Take a moment to process what just happened before reacting.
Unexpected moments often lead to the biggest opportunities.
Stay adaptable — not everything needs an immediate response.
Embrace the unexpected. Life's best chapters are often unplanned. 🌟""",

    "disgust": """It is okay to feel uncomfortable — your instincts are valid.
Calmly remove yourself from the situation if possible.
Reflect on what specifically triggered this feeling.
Set boundaries where needed. Protecting your peace is a priority. 🍃""",

    "neutral": """You seem calm and mentally balanced right now.
This is actually the best state to make clear decisions.
Use this focused energy to tackle something important today.
Consistency in a calm state builds long-term success. ✅""",

    "anxiety": """Start by focusing on your breathing — inhale for 4 seconds, exhale for 4.
Write down your worries so they feel smaller and more manageable.
Avoid overthinking by focusing only on what you can control right now.
Remember: most things you worry about never actually happen. 🌿""",

    "excitement": """That energy you feel right now is incredibly powerful — use it.
Channel your excitement into planning and taking action.
Share your excitement with someone who will celebrate with you.
Ride this wave — motivation at its peak leads to incredible results. 🚀""",

    "love": """Love is one of the strongest human emotions — cherish it.
Express how you feel to the people who matter most to you.
Small gestures mean more than grand ones — be present and genuine.
Love grows when you give it freely and without expectation. ❤️""",

    "gratitude": """Take a moment to fully appreciate what you have right now.
Write down three things you are grateful for today.
Express your gratitude to someone who has impacted your life.
A grateful mindset attracts more positive experiences. 🙏""",

    "loneliness": """Loneliness is temporary — connection is always possible.
Reach out to one person today, even just a simple message.
Spend time doing something you genuinely enjoy solo first.
Community is everywhere — sometimes you just have to take the first step. 🤝"""
}

def get_suggestion(emotion):
    # Convert emotion to lowercase and look it up in the dictionary
    # If emotion not found, return a default message
    return suggestions.get(emotion.lower(), """Take a moment to check in with yourself.
Whatever you are feeling is valid and worth acknowledging.
Be kind to yourself today — that is always the right move.
If needed, talk to someone you trust about how you are doing. 🌿""")
