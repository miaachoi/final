import csv

filename = "data/journal.csv"

def save_entry(entries):
    try: 
        with open(filename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["date", "text", "mood"])
            writer.writeheader()
            writer.writerows(entries)
    except Exception as e: 
        print(f"Error saving entries: {e}")

def load_entries():
   try:
       with open(filename, mode="r") as file:
           reader = csv.DictReader(file)
           entries = list(reader) 

           valid_entries = []

           for entry in entries:
               if all(field in entry for field in ["date", "text", "mood"]):
                   valid_entries.append(entry)
               else: 
                   print("Warning: Skipping an entry due to missing fields.") 

           return valid_entries
       
   except FileNotFoundError:
       print("No previous journal entries found. Starting fresh.") 
       return []
   except Exception as e: 
       print(f"Error loading entries: {e}")
       return [] 