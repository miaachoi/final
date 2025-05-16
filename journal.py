from datetime import datetime 
from mood_analysis import analyze_mood
from file_operations import save_entry, load_entries
from utils import get_today_date
import requests
import pandas as pd

class BaseEntry: 
    def __init__(self, text, date): 
        self.text = text
        self.date = date

    def summarize(self): 
        return self.text[:50] + "..."

class JournalEntry(BaseEntry): 
    def __init__(self, text, date, mood): 
        super().__init__(text, date) 
        self.mood = mood

    def summarize(self): 
        return f"{self.date} | {self.mood} | {self.text[:60]}..."
    
class JournalManager: 
    def __init__(self):
        self.entries = []

    def add_entry(self, entry): 
        self.entries.append(entry) 
    
    def delete_entry(self, index): 
        if 0 <= index < len(self.entries): 
            del self.entries[index]
    
    def get_entries(self): 
        return self.entries
    
    def display_entries(self): 
        for entry in self.entries: 
            print(entry.summarize())

    def export_to_csv_format(self): 
        return [(e.date, e.mood, e.text) for e in self.entries]
    
    def describe_mood_data(self): 
        if not self.entries: 
            print("No data available.")
            return 
        
        data = pd.DataFrame(self.export_to_csv_format(), columns=["date", "mood", "text"])
        mood_counts = data["mood"].value_counts() 

        print("\nMood Frequency Table:")
        print(mood_counts.to_string())

        print("\nMood Statistics (count, unique, top, freq):")
        print(data["mood"].describe())

def get_daily_quote(): 
    try: 
        response = requests.get("https://zenquotes.io/api/random", timeout=5)
        if response.status_code == 200: 
            data = response.json()[0]
            return f"{data['q']} - {data['a']}"
    except Exception as e: 
        print("Failed to fetch quote:", e)
    return None

def run_journal(): 
    raw_entries = load_entries() 
    manager = JournalManager() 

    for e in raw_entries: 
        manager.add_entry(JournalEntry(e['text'], e['date'], e['mood']))

    while True: 
        print("\n1. New Entry\n2. View Entries\n3. Mood Data Summary\n4. Get Daily Quote\n5. Quit")
        choice = input("Choose an option: ")

        if choice == "1":
            text = input("Write your journal entry:\n")
            date = get_today_date() 

            tag_manually = input("Would you like to tag your mood manually? (yes/no): ").strip().lower()
            if tag_manually == "yes":
                mood = input("Enter your mood tag (e.g., happy, sad, anxious): ").strip().lower() 
            else: 
                mood = analyze_mood(text) 

            entry = JournalEntry(text, date, mood) 
            manager.add_entry(entry) 
            print(f"Mood: {mood}")
            print("Entry logged successfully!")
            save_entry([{"text": e.text, "date": e.date, "mood": e.mood} for e in manager.get_entries()])

        elif choice == "2": 
            manager.display_entries() 

        elif choice == "3": 
            manager.describe_mood_data()

        elif choice == "4":
            quote = get_daily_quote() 
            if quote: 
                print(f"\nHere's your quote for today:\n{quote}") 
        
        elif choice == "5":
            break 

        else: 
            print("Invalid choice. Try again.") 