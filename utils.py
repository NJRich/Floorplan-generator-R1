import re

def parse_prompt(prompt: str, room_database: dict) -> list:
    room_list = []
    prompt_lower = prompt.lower()

    for key in room_database:
        # Match plural and singular (e.g. "exam room", "exam rooms")
        pattern = rf'(\d+)\s+{room_database[key]["name"].lower()}s?'
        match = re.search(pattern, prompt_lower)
        if match:
            count = int(match.group(1))
            room_list.extend([key] * count)

    return room_list
