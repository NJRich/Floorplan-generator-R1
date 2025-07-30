import re
import json
import os

def singularize(word):
    word = word.lower().strip()
    if word.endswith("ies"):
        return word[:-3] + "y"
    elif word.endswith("sses") or word.endswith("shes") or word.endswith("ches"):
        return word[:-2]
    elif word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word

def load_room_database(json_path="room_database.json"):
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"{json_path} not found")
    with open(json_path, "r") as f:
        room_data = json.load(f)

    normalized_data = {}
    for key, value in room_data.items():
        normalized_key = key.lower().strip().replace(" ", "_")
        normalized_data[normalized_key] = value
    return normalized_data

def parse_prompt(prompt, room_data=None):
    prompt = prompt.lower()
    room_counts = {}

    if room_data is None:
        room_data = load_room_database()

    # Force raw check for keywords
    keywords = {
        "patient room": "patient_room",
        "nurse station": "nurse_station",
        "dirty utility": "dirty_utility"
    }

    for phrase, key in keywords.items():
        if phrase in prompt:
            match = re.search(r'(\d+)\s+' + re.escape(phrase), prompt)
            count = int(match.group(1)) if match else 1
            room_counts[key] = count
            print(f"[✓] Force matched: '{phrase}' → {key} × {count}")

    print("🧾 TEMP parsed room counts:", room_counts)
    return room_counts
