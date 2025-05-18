import re

MOOD_KEYWORDS = {
   "happy": ["happy", "joy", "excited", "grateful", "glad", "cheerful", "content", "delighted"],
   "sad": ["sad", "depressed", "unhappy", "down", "crying", "gloomy", "heartbroken", "hopeless"],
   "angry": ["angry", "mad", "furious", "upset", "frustrated", "annoyed", "irritated", "enraged"],
   "anxious": ["nervous", "worried", "anxious", "tense", "stressed", "panicked", "overwhelmed", "uneasy"]
}


def analyze_mood(text):
   text = text.lower()
   mood_scores = {mood: 0 for mood in MOOD_KEYWORDS}
   for mood, keywords in MOOD_KEYWORDS.items():
       for word in keywords:
           matches = re.findall(rf'\b{word}\b', text)
           mood_scores[mood] += len(matches)
   return max(mood_scores, key=mood_scores.get) if any(mood_scores.values()) else "neutral"