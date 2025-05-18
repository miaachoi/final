import pytest
from file_operations import save_entry, load_entries
import os 

def test_save_and_load():
   filename = "data/journal.csv" 
   if os.path.exists(filename): 
      os.remove(filename) 

   test_entries = [
      {"date": "2025-04-29", "text": "Testing file ops", "mood": "neutral"},
      {"date": "2025-04-30", "text": "Another test entry", "mood": "happy"}
   ]
   save_entry(test_entries)

   loaded_entries = load_entries()
   
   assert len(loaded_entries) == len(test_entries), "The number of loaded entries doesn't match the number of saved entries."

   for i, entry in enumerate(test_entries): 
      assert loaded_entries[i]["date"] == entry["date"], f"Entry {i} has incorrect date."
      assert loaded_entries[i]["text"] == entry["text"], f"Entry {i} has incorrect text."
      assert loaded_entries[i]["mood"] == entry["mood"], f"Entry {i} has incorrect mood."

def test_load_entries_empty(): 
   filename = "data/journal.csv"
   if os.path.exists(filename): 
      os.remove(filename) 

   entries = load_entries()

   assert len(entries) == 0, "Entries should by empty when the file is empty."

def test_load_entries_with_data(): 
    filename = "data/journal.csv"
    test_entries = [
       {"date": "2025-05-10", "text": "Test entry", "mood": "happy"}
    ]
    save_entry(test_entries)

    entries = load_entries() 

    assert len(entries) > 0, "Entries should not be empty"
    assert all("date" in entry and "text" in entry for entry in entries), "Each entry should have 'date' and 'text'" 