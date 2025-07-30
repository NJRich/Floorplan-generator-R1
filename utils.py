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

    known_rooms = list(room_data.keys())  # e.g. patient_room, nurse_station

    # Pre-clean: replace "an"/"a" with 1 to simplify
    prompt = re.sub(r'\b(an|a)\b', '1', prompt)

    # Loop through known room types and match them in prompt
    for key in known_rooms:
        # Turn patient_room → patient room for matching
        room_phrase = key.replace("_", " ")

        match = re.search(rf'(\d+)\s+{re.escape(room_phrase)}', prompt)
        if match:
            count = int(match.group(1))
            room_counts[key] = count
            print(f"[✓] Matched: {room_phrase} → {key} × {count}")
        elif room_phrase in prompt:
            # No number, default to 1
            room_counts[key] = room_counts.get(key, 0) + 1
            print(f"[•] Inferred: {room_phrase} → {key} × 1")

    print("🧾 Final parsed room counts:", room_counts)
    return room_counts
