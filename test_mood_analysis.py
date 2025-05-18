import pytest
from mood_analysis import analyze_mood

def test_analyze_mood_valid(): 
   text = "I am so happy today!"
   assert analyze_mood(text) == "happy", "Mood analysis failed for valid input."
   
def test_analyze_mood_empty(): 
   text = ""
   assert analyze_mood(text) == "neutral", "Mood analysis failed for empty input."

def test_analyze_mood(): 
   text = "I am feeling so happy and excited!" 
   mood = analyze_mood(text) 
   assert mood == "happy", "The mood should be 'happy' based on the input text"

   text = "I feel sad and down today."
   mood = analyze_mood(text) 
   assert mood == "sad", "The mood should be 'sad' based on the input text"

   text = "I am so mad right now!" 
   mood = analyze_mood(text) 
   assert mood == "angry", "The mood should be 'angry' based on the input text" 

   text = "I am not really doing anything. Just doing some work."
   mood = analyze_mood(text)
   assert mood == "neutral", "The mood should be 'neutral' based on the input text"