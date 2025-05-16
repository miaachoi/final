import csv

filename = "data/journal.csv"

def save_entry(entries):
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "text", "mood"])
        writer.writeheader()
        writer.writerows(entries) 

def load_entries():
    try:
        with open(filename, mode="r") as file: 
            reader = csv.DictReader(file) 
            return list(reader)
    except FileNotFoundError:
        return []