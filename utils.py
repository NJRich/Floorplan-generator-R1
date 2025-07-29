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
        room_data = json.load(f)
    return {singularize(k.lower().replace(" ", "_")): v for k, v in room_data.items()}

def parse_prompt(prompt, room_data=None):
    prompt = prompt.lower()
    room_counts = {}

    if room_data is None:
        room_data = load_room_database()

    # Match phrases like "3 exam rooms", "a pantry", "one lobby"
    matches = re.findall(r'(\d+|a|an|one)\s+([a-zA-Z_ ]+?)(?:s|room|rooms)?(?:,|\.|\s|$)', prompt)

    for count_str, room_str in matches:
        cleaned_room = singularize(room_str.strip().replace(" ", "_"))

        # Convert "a", "an", "one" to 1
        if count_str in ["a", "an", "one"]:
            count = 1
        else:
            count = int(count_str)

        if cleaned_room in room_data:
            room_counts[cleaned_room] = room_counts.get(cleaned_room, 0) + count
        else:
            print(f"[!] Warning: Room '{room_str.strip()}' → '{cleaned_room}' not in room_database.json")

    print("🔎 Raw matches found:", matches)
    print("✅ Cleaned & matched room counts:", room_counts)
    return room_counts
