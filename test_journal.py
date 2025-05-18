import pytest
import os 
from file_operations import save_entry, load_entries
from journal import JournalManager, JournalEntry

def test_add_entry(): 
    manager = JournalManager()
    initial_count = len(manager.get_entries())
    manager.add_entry(JournalEntry("Test entry", "2025-04-30", "happy"))
    assert len(manager.get_entries()) == initial_count + 1, "Entry was not added properly."

def test_update_entry(): 
    manager = JournalManager() 
    entry = JournalEntry("Initial entry", "2025-05-10", "sad")
    manager.add_entry(entry) 

    manager.get_entries()[0].text = "Updated text" 
    assert manager.get_entries()[0].text == "Updated text", "Text update failed."

    manager.get_entries()[0].mood = "happy"
    assert manager.get_entries()[0].mood == "happy", "Mood update failed." 

def test_delete_entry(): 
    manager = JournalManager() 
    entry = JournalEntry("Test entry", "2025-05-10", "happy")
    manager.add_entry(entry) 
    initial_count = len(manager.get_entries())
    manager.delete_entry(0)
    assert len(manager.get_entries()) == initial_count - 1, "Entry was not deleted properly."

def test_load_entries(): 
    filename = "data/journal.csv" 
    if os.path.exists(filename): 
        os.remove(filename) 

    test_entries = [{"date": "2025-05-10", "text": "Test entry", "mood": "happy"}]
    save_entry(test_entries) 

    loaded_entries = load_entries() 

    assert loaded_entries, "Entries should be loaded properly."
    assert loaded_entries[0]["text"] == "Test entry", "Loaded entry text is incorrect."
    assert loaded_entries[0]["mood"] == "happy", "Loaded entry mood is incorrect." 