import re

def parse_prompt(prompt):
    """
    Very basic NLP parser that extracts room names and quantities from a user prompt.
    Returns a list of dictionaries: [{name, width, depth}, ...]
    """
    # Default room sizes (width, depth) in feet
    default_sizes = {
        "exam room": (10, 13),
        "waiting area": (12, 12),
        "cafe": (15, 15),
        "lobby": (18, 18),
        "staff open office": (20, 15),
        "pantry": (10, 10),
        "conference room": (16, 14),
        "private office": (10, 12)
    }

    results = []

    prompt = prompt.lower()

    for room in default_sizes:
        # Match quantities like "2 exam rooms", "1 pantry", etc.
        plural = room + "s" if not room.endswith("s") else room
        pattern = r'(\d+)\s+' + re.escape(plural)
        matches = re.findall(pattern, prompt)
        count = sum(int(m) for m in matches) if matches else 0

        if count == 0:
            # If prompt just says "pantry" (no number), assume 1
            if room in prompt or plural in prompt:
                count = 1

        for i in range(count):
            name = f"{room.title()} {i+1}" if count > 1 else room.title()
            width, depth = default_sizes[room]
            results.append({
                "name": name,
                "width": width,
                "depth": depth
            })

    return results

