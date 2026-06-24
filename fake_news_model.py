# fake_news_model.py
# This file uses NewsAPI to check if a news headline is real
# by searching it across 150,000+ real news sources worldwide

import requests

NEWS_API_KEY = "3f8b2ef9613e4cdb909dbe08784a351c"

def load_fake_news_model():
    # No model to load, we use NewsAPI instead
    return None

def analyze_news(text, model=None):
    # Send the headline to NewsAPI and search for it
    url = "https://newsapi.org/v2/everything"
    
    params = {
        "q": text,
        "apiKey": NEWS_API_KEY,
        "pageSize": 5,
        "language": "en"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        total_results = data.get("totalResults", 0)
        articles = data.get("articles", [])
        
        if total_results >= 3:
            # Found in multiple real news sources = REAL
            source_names = [a['source']['name'] for a in articles[:3]]
            return "REAL", 0.92, total_results, source_names
        elif total_results >= 1:
            # Found in at least one source = possibly real
            source_names = [a['source']['name'] for a in articles[:3]]
            return "REAL", 0.65, total_results, source_names
        else:
            # Not found anywhere = likely fake
            return "FAKE", 0.85, 0, []
            
    except Exception as e:
        return "UNKNOWN", 0.0, 0, []
