import json
from PIL import Image, ImageDraw
import math
import re
import os


def load_room_database(json_path="room_database.json"):
    with open(json_path, "r") as f:
        return json.load(f)


def parse_prompt(prompt, room_database):
    prompt = prompt.lower().replace(" and ", ", ")
    parts = [p.strip() for p in re.split(r'[;,]', prompt) if p.strip()]
    
    num_words = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
    }

    rooms = []
    for part in parts:
        tokens = part.split()
        if not tokens:
            continue
        count = 1
        if tokens[0] in num_words:
            count = num_words[tokens[0]]
            tokens = tokens[1:]
        elif tokens[0].isdigit():
            count = int(tokens[0])
            tokens = tokens[1:]
        elif tokens[0] in ("a", "an"):
            count = 1
            tokens = tokens[1:]
        room_type = " ".join(tokens)
        if room_type.endswith("s") and room_type[:-1] in room_database:
            room_type = room_type[:-1]
        if room_type in room_database:
            size = room_database[room_type]
            for _ in range(count):
                rooms.append((room_type, size["width_ft"], size["depth_ft"]))
    return rooms


def draw_floorplan(rooms, corridor_width=6.0, wall_thickness=0.5, scale=10):
    margin = 20
    wall_px = int(wall_thickness * scale)
    
    # Split into two rows
    half = len(rooms) // 2 + len(rooms) % 2
    top = rooms[:half]
    bottom = rooms[half:]

    top_depth = max(r[2] for r in top) if top else 0
    bottom_depth = max(r[2] for r in bottom) if bottom else 0
    plan_width = max(sum(r[1] for r in top), sum(r[1] for r in bottom))
    plan_height = top_depth + bottom_depth + corridor_width

    img_w = int((plan_width + 2 * wall_thickness) * scale) + 2 * margin
    img_h = int((plan_height + 2 * wall_thickness) * scale) + 2 * margin

    image = Image.new("RGB", (img_w, img_h), "white")
    draw = ImageDraw.Draw(image)

    offset_x = margin + wall_px
    offset_y = margin + wall_px

    def draw_row(row, y_start_ft):
        x_cursor_ft = 0.0
        for i, (name, w_ft, d_ft) in enumerate(row):
            x1 = offset_x + int(x_cursor_ft * scale)
            y1 = offset_y + int(y_start_ft * scale)
            x2 = x1 + int(w_ft * scale)
            y2 = y1 + int(d_ft * scale)
            draw.rectangle([x1, y1, x2, y2], fill="#e6f2ff", outline="black", width=wall_px)
            draw.text((x1 + 4, y1 + 4), name[:1].upper(), fill="black")
            x_cursor_ft += w_ft

    draw_row(top, 0)
    draw_row(bottom, top_depth + corridor_width)

    # Draw corridor
    cy1 = offset_y + int(top_depth * scale)
    cy2 = cy1 + int(corridor_width * scale)
    cx1 = offset_x
    cx2 = offset_x + int(plan_width * scale)
    draw.rectangle([cx1, cy1, cx2, cy2], fill="lightgray")

    return image
