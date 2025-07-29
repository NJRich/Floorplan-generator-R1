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

    # Normalize keys
    return {singularize(k.lower().replace(" ", "_")): v for k, v in room_data.items()}

# === NLP-style prompt parser ===
def parse_prompt(prompt, room_data=None):
    prompt = prompt.lower()
    room_counts = {}

    if room_data is None:
        room_data = load_room_database()

    # Match numeric: "3 exam rooms"
    numeric_matches = re.findall(r'(\d+)\s+([a-zA-Z_ ]+?)(?:s|room|rooms)?(?:,|\.|\s|$)', prompt)

    # Match articles: "a pantry", "an exam room"
    article_matches = re.findall(r'\b(a|an)\s+([a-zA-Z_ ]+?)(?:s|room|rooms)?(?:,|\.|\s|$)', prompt)

    for count_str, room_str in numeric_matches:
        count = int(count_str)
        cleaned_room = singularize(room_str.strip().replace(" ", "_"))
        if cleaned_room in room_data:
            room_counts[cleaned_room] = room_counts.get(cleaned_room, 0) + count
        else:
            print(f"[!] Warning: Room '{room_str.strip()}' → '{cleaned_room}' not in room_database.json")

    for _, room_str in article_matches:
        cleaned_room = singularize(room_str.strip().replace(" ", "_"))
        if cleaned_room in room_data:
            room_counts[cleaned_room] = room_counts.get(cleaned_room, 0) + 1
        else:
            print(f"[!] Warning: Room '{room_str.strip()}' → '{cleaned_room}' not in room_database.json")

    print("🔎 Raw numeric matches:", numeric_matches)
    print("🔎 Raw article matches:", article_matches)
    print("✅ Parsed room counts:", room_counts)
    return room_counts
