import re
import json
import os

def singularize(noun):
    noun = noun.lower().strip()
    if noun.endswith("ies"):
        return noun[:-3] + "y"
    elif noun.endswith("sses") or noun.endswith("shes") or noun.endswith("ches"):
        return noun[:-2]
    elif noun.endswith("s") and not noun.endswith("ss"):
        return noun[:-1]
    return noun

def load_room_database(json_path="room_database.json"):
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"{json_path} not found")

    with open(json_path, "r") as f:
        raw_data = json.load(f)

    # Normalize to match prompt structure
    normalized_data = {}
    for key, val in raw_data.items():
        clean_key = singularize(key.lower().replace(" ", "_").replace("/", "_"))
        normalized_data[clean_key] = val
        val["_lookup_keys"] = [clean_key]

        # Support additional fallback names (e.g., "exam", "procedure", etc.)
        short_key = singularize(val["name"].lower().replace(" ", "_").split("_")[0])
        if short_key not in normalized_data:
            normalized_data[short_key] = val
            val["_lookup_keys"].append(short_key)

    return normalized_data

def parse_prompt(prompt, room_data=None):
    prompt = prompt.lower()
    room_counts = {}

    if room_data is None:
        room_data = load_room_database()

    matches = re.findall(r'(\d+)\s+([a-zA-Z_ ]+?)(?:s|room|rooms)?(?:,|\.|\s|$)', prompt)

    for count_str, room_str in matches:
        count = int(count_str)
        cleaned_room = singularize(room_str.strip().replace(" ", "_"))

        matched = False
        for db_key, data in room_data.items():
            if cleaned_room in data.get("_lookup_keys", []):
                room_counts[db_key] = room_counts.get(db_key, 0) + count
                matched = True
                break

        if not matched:
            print(f"[!] Warning: Room '{room_str.strip()}' → '{cleaned_room}' not matched in database.")

    print("🔎 Raw matches found:", matches)
    print("✅ Cleaned & matched room counts:", room_counts)
    return room_counts
