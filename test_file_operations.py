from file_operations import save_entry, load_entries

def test_save_and_load():
    test_entries = [{"date": "2025-04-29", "text": "Testing file ops", "mood": "neutral"}]
    save_entry(test_entries)
    loaded = load_entries()
    assert loaded[0]["text"] == "Testing file ops"