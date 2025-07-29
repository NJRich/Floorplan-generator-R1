import re

def parse_prompt(prompt):
    """
    Extracts room types and quantities from a natural language prompt.

    Example input: "A hospital with 2 procedure rooms and 5 patient rooms and a lobby"
    Output: [("Procedure Room", 2), ("Patient Room", 5), ("Lobby", 1)]
    """
    prompt = prompt.lower()
    # Normalize common phrases
    prompt = prompt.replace("a ", "1 ").replace("an ", "1 ")

    # Match room phrases like "3 exam rooms", "1 lobby"
    pattern = r'(\d+)\s+([a-z\s]+?)(?:s|room|rooms)?(?=,| and|$)'
    matches = re.findall(pattern, prompt)

    rooms = []
    for count, name in matches:
        name = name.strip().replace("room", "").replace("area", "").title()
        if not name.endswith("Room") and name.lower() not in ["lobby", "pantry", "cafe", "reception"]:
            name += " Room"
        rooms.append((name.strip(), int(count)))

    return rooms
