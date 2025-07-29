def parse_prompt(prompt, room_data=None):
    import re
    prompt = prompt.lower()
    room_counts = {}

    if room_data is None:
        room_data = load_room_database()

    # Match numeric counts: e.g. "2 exam rooms"
    numeric_matches = re.findall(r'(\d+)\s+([a-zA-Z_ ]+?)(?:s|room|rooms)?(?:,|\.|\s|$)', prompt)

    # Match "a"/"an" cases: e.g. "a pantry", "an exam room"
    article_matches = re.findall(r'\b(a|an)\s+([a-zA-Z_ ]+?)(?:s|room|rooms)?(?:,|\.|\s|$)', prompt)

    # Process numeric matches
    for count_str, room_str in numeric_matches:
        count = int(count_str)
        cleaned_room = singularize(room_str.strip().replace(" ", "_"))
        if cleaned_room in room_data:
            room_counts[cleaned_room] = room_counts.get(cleaned_room, 0) + count
        else:
            print(f"[!] Warning: Room '{room_str.strip()}' → '{cleaned_room}' not in room_database.json")

    # Process "a"/"an" matches as count = 1
    for article, room_str in article_matches:
        cleaned_room = singularize(room_str.strip().replace(" ", "_"))
        if cleaned_room in room_data:
            room_counts[cleaned_room] = room_counts.get(cleaned_room, 0) + 1
        else:
            print(f"[!] Warning: Room '{room_str.strip()}' → '{cleaned_room}' not in room_database.json")

    print("🔎 Raw numeric matches:", numeric_matches)
    print("🔎 Raw article matches:", article_matches)
    print("✅ Parsed room counts:", room_counts)
    return room_counts
