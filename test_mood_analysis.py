import pytest
from mood_analysis import analyze_mood

def test_happy_mood():
    assert analyze_mood("I am so happy and excited!") == "happy"

def test_sad_mood():
    assert analyze_mood("I feel sad and down today.") == "sad"