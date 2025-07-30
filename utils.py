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

    known_rooms = list(room_data.keys())
    print("📦 Known room types:", known_rooms)

    # Match examples like: "20 patient rooms", "a nurse station", "1 dirty utility"
    pattern = r'(?:(\d+)|\ba\b|\ban\b)?\s*([a-zA-Z ]+?)(?:s| room| rooms)?(?=,|\.|\s|$)'
    matches = re.findall(pattern, prompt)
    print("🔍 Matches found:", matches)

    for count_str, raw_room in matches:
        count = int(count_str) if count_str else 1

        # Clean up room name
        words = raw_room.strip().lower().split()
        if not words:
            continue

        words[-1] = singularize(words[-1])  # Only singularize last word
        cleaned = "_".join(words)  # e.g., "nurse station" → "nurse_station"

        matched = None
        if cleaned in room_data:
            matched = cleaned
        elif f"{cleaned}_room" in room_data:
            matched = f"{cleaned}_room"
        else:
            for r in known_rooms:
                if cleaned.replace("_", "") == r.replace("_", ""):
                    matched = r
                    break

        if matched:
            room_counts[matched] = room_counts.get(matched, 0) + count
            print(f"[✓] Matched '{raw_room.strip()}' → '{matched}'")
        else:
            print(f"[!] Skipped: '{raw_room.strip()}' → '{cleaned}' not found in room database.")

    print("🧾 Final parsed room counts:", room_counts)
    return room_counts
