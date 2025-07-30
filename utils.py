import re
import json
import os

# === Singularization helper ===
def singularize(noun):
    noun = noun.lower().strip()
    if noun.endswith("ies"):
        return noun[:-3] + "y"
    elif noun.endswith("sses") or noun.endswith("shes") or noun.endswith("ches"):
        return noun[:-2]
    elif noun.endswith("s") and not noun.endswith("ss"):
        return noun[:-1]
    return noun

# === Load room types from room_database.json ===
def load_room_database(json_path="room_database.json"):
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"{json_path} not found")
    with open(json_path, "r") as f:
        room_data = json.load(f)

    # Normalize keys: exam room → exam_room
    normalized_data = {}
    for key, value in room_data.items():
        normalized_key = singularize(key.lower().replace(" ", "_"))
        normalized_data[normalized_key] = value

    return normalized_data

# === NLP-style prompt parser ===
def parse_prompt(prompt, room_data=None):
    prompt = prompt.lower()
    room_counts = {}

    if room_data is None:
        room_data = load_room_database()

    known_rooms = list(room_data.keys())

    # Match examples like:
    # - "3 patient rooms"
    # - "a pantry"
    # - "1 nurse station"
    pattern = r'(?:(\d+)|\ba\b|\ban\b)?\s*([a-zA-Z ]+?)(?:s| room| rooms)?(?=,|\.|\s|$)'
    matches = re.findall(pattern, prompt)

    for count_str, raw_room in matches:
        count = int(count_str) if count_str else 1
        room_candidate = singularize(raw_room.strip().replace(" ", "_"))

        matched = None

        # Try exact match
        if room_candidate in room_data:
            matched = room_candidate
        # Try with _room suffix
        elif f"{room_candidate}_room" in room_data:
            matched = f"{room_candidate}_room"
        # Try fuzzy match by removing underscores
        else:
            for r in known_rooms:
                if room_candidate.replace("_", "") == r.replace("_", ""):
                    matched = r
                    break

        if matched:
            room_counts[matched] = room_counts.get(matched, 0) + count
        else:
            print(f"[!] Skipped: '{raw_room.strip()}' → '{room_candidate}' not found in room database.")

    print("🧾 Parsed room counts:", room_counts)
    return room_counts
