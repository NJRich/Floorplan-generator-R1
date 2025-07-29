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

    # Match phrases like "3 exam rooms", "a pantry", "1 restroom", etc.
    matches = re.findall(r'(?:(\d+)|\ba\b|\ban\b)?\s*([a-zA-Z_ ]+?)(?:s|room|rooms)?(?:,|\.|\s|$)', prompt)

    for count_str, room_str in matches:
        count = int(count_str) if count_str else 1
        base = singularize(room_str.strip().replace(" ", "_"))

        # Try exact match
        if base in room_data:
            cleaned = base
        # Try appending '_room' if needed
        elif f"{base}_room" in room_data:
            cleaned = f"{base}_room"
        # Try matching just the base word
        elif base.replace("_", "") in [k.replace("_", "") for k in room_data]:
            cleaned = next(k for k in room_data if k.replace("_", "") == base.replace("_", ""))
        else:
            print(f"[!] Warning: Room '{room_str.strip()}' → '{base}' not in room_database.json — skipped.")
            continue

        room_counts[cleaned] = room_counts.get(cleaned, 0) + count

    print("🧾 Parsed room counts:", room_counts)
    return room_counts
