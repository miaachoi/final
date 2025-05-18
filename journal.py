import matplotlib.pyplot as plt
from datetime import datetime
from mood_analysis import analyze_mood
from file_operations import save_entry, load_entries
from utils import get_today_date
from collections import defaultdict
from mood_analysis import MOOD_KEYWORDS
import requests
import pandas as pd

def plot_mood_trends(entries): 
    mood_counts = defaultdict(int) 

    for entry in entries: 
        mood_counts[entry.mood] += 1

    plt.bar(mood_counts.keys(), mood_counts.values())
    plt.xlabel('Mood')
    plt.ylabel('Frequency')
    plt.title('Mood Frequency Over Time')
    plt.show() 

class BaseEntry: 
    """Base class for a journal entry containing text and date."""

    def __init__(self, text, date): 
        """
        Initialize a base entry.

        Parameters: 
        text (str): The content of the journal entry.
        date (str): The date of the entry. 
        """
        self.text = text
        self.date = date 

    def summarize(self): 
        """
        Return a brief summary of the entry text.

        Returns: 
        str: First 50 characters of text followed by ellipsis. 
        """
        return self.text[:50] + "..."

class JournalEntry(BaseEntry):
    """Extended journal entry with mood information."""

    def __init__(self, text, date, mood): 
        """
        Initialize a journal entry.

        Parameters: 
        text (str): The content of the journal entry.
        date (str): The date of the entry.
        mood (str): The mood associated with the entry. 
        """

        super().__init__(text, date) 
        self.mood = mood

    def summarize(self): 
        """
        Return a detailed summary including date, mood, and preview of the entry.

        Returns: 
        str: Formatted string with date, mood, and preview. 
        """
        return f"{self.date} | {self.mood} | {self.text[:60]}..."
    
class JournalManager: 
    """Manages a collection of journal entries."""

    def __init__(self): 
        """Initialize the journal manager with an empty list of entries."""
        self.entries = []
    
    def add_entry(self, entry):
        """
        Add a new journal entry.

        Parameters: 
        entry (JournalEntry): The journal entry to add.
        """
        self.entries.append(entry) 

    def delete_entry(self, index): 
        """
        Delete a journal entry by index.

        Parameters: 
        index (int): The index of the entry to delete.
        """
        if 0 <= index < len(self.entries): 
            del self.entries[index]
    
    def get_entries(self): 
        """
        Get all journal entries.

        Returns: 
        list: List of JournalEntry objects.
        """
        return self.entries

    def display_entries(self): 
        """Print summaries of all journal entries."""
        for i, entry in enumerate(self.entries): 
            print(f"{i}. {entry.summarize()}")
        
    def export_to_csv_format(self): 
        """
        Export entries to a list suitable for CSV output. 

        Returns: 
        list of tuples: Each tuple contains (date, mood, text)
        """
        return [(e.date, e.mood, e.text) for e in self.entries]
    
    def describe_mood_data(self): 
        """Print summary statistics and frequency counts of moods."""
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
    """
    Gets a random daily quote from ZenQuotes API.

    Returns: 
    str or None: Quote text with author, or None if failed. 
    """
    try: 
        response = requests.get("https://zenquotes.io/api/random", timeout=5)
        if response.status_code == 200: 
            data = response.json()[0]
            return f"{data['q']} - {data['a']}"
    except Exception as e: 
        print(f"Failed to fetch quote: {e}. Please try again later.")
    return None

def run_journal(): 
    """Main loop for interacting with the journal application."""
    raw_entries = load_entries() 
    manager = JournalManager() 

    for e in raw_entries: 
        manager.add_entry(JournalEntry(e['text'], e['date'], e['mood']))

    while True: 
        print("\n1. New Entry\n2. View Entries\n3. Mood Data Summary\n4. Get Daily Quote\n5. Delete an Entry\n6. Update an Entry\n7. Quit")
        choice = input("Choose an option: ").strip() 

        if choice not in ["1", "2", "3", "4", "5", "6", "7"]:
            print("Invalid option. Please choose a valid option.")
            continue 

        if choice == "1":
            text = input("Write your journal entry:\n")
            date = get_today_date() 

            tag_manually = input("Would you like to tag your mood manually? (yes/no): ").strip().lower() 
            
            if tag_manually == "yes": 
                
                while True: 
                    mood = input("Enter your mood tag (e.g., happy, sad, anxious, angry): ").strip().lower() 
                    
                    if mood in MOOD_KEYWORDS: 
                        break
                    else:
                        print("Invalid mood tag. Please enter one of the supported moods (e.g., happy, sad, anxious).")
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
            plot_mood_trends(manager.get_entries()) 

        elif choice == "4":
            quote = get_daily_quote() 
            if quote: 
                print(f"\nHere's your quote for today:\n{quote}")
        
        elif choice == "5": 
            try: 
                manager.display_entries() 
                index = int(input("Enter the index of the entry to delete: "))

                confirm_delete = input(f"Are you sure you want to delete this entry {index}? (yes/no): ").strip().lower() 
                if confirm_delete == "yes": 
                    manager.delete_entry(index)
                    print(f"Entry {index} deleted successfully!")
                    save_entry([{"text": e.text, "date": e.date, "mood": e.mood} for e in manager.get_entries()])
                else: 
                    print("Entry not deleted.") 

            except ValueError:
                print("Invalid input. Please enter a valid index number.")
            except IndexError: 
                print("Invalid index. Please enter a valid entry index.") 

        elif choice == "6":
            try: 
                manager.display_entries() 
                index = int(input("Enter the index of the entry to update: "))
                entry = manager.get_entries()[index]
                print(f"Current Entry: {entry.summarize()}")

                update_choice = input("Would you like to update the text or the mood? (text/mood): ").strip().lower() 

                if update_choice == "text":
                    new_text = input("Enter the new text for your journal entry:\n")
                    entry.text = new_text
                elif update_choice == "mood": 
                    new_mood = input("Enter the new mood for your journal entry:\n").strip().lower() 
                    if new_mood in MOOD_KEYWORDS: 
                        entry.mood = new_mood 
                    else: 
                        print("Invalid mood tag. Please choose from the following: {', '.join(MOOD_KEYWORDS)}") 
                        continue 
                else: 
                    print("Invalid option. Please choose either 'text' or 'mood'.") 
                    continue 
                
                save_entry([{"text": e.text, "date": e.date, "mood": e.mood} for e in manager.get_entries()])
                print(f"Entry {index} updated successfully!") 
                manager.display_entries() 

            except ValueError: 
                print("Invalid index. Please enter a valid entry index.") 
            except IndexError: 
                print("Invalid index. No entry found with that index.") 

        elif choice == "7":
            print("See you next time!")
            break