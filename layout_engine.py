 if not parsed_prompt:
        print("❌ No valid rooms parsed from prompt.")
        return None

    print("🔍 Generating layout for rooms:", parsed_prompt)
import json
from PIL import Image, ImageDraw

# Load the room database
with open("room_database.json", "r") as f:
    ROOM_DATABASE = json.load(f)

def generate_layout_image(parsed_rooms, scale=10, wall_thickness_ft=0.5, corridor_width_ft=6.0):
    """
    Takes parsed rooms and returns a Pillow image with a basic floor plan.
    """
    wall_px = int(wall_thickness_ft * scale)
    margin = 20
    top_row = []
    bottom_row = []

    # Build list of (name, width_ft, height_ft)
    room_list = []
    for room_type, count in parsed_rooms:
        if room_type in ROOM_DATABASE:
            width, height = ROOM_DATABASE[room_type]["size_ft"]
            for i in range(count):
                label = f"{room_type} {i+1}" if count > 1 else room_type
                room_list.append((label, width, height))
        else:
            print(f"⚠️ Room type not found: {room_type}")

    # Simple even split layout
    mid = len(room_list) // 2
    top_row = room_list[:mid]
    bottom_row = room_list[mid:]

    # Calculate canvas size
    top_width = sum(r[1] for r in top_row)
    bottom_width = sum(r[1] for r in bottom_row)
    canvas_width_ft = max(top_width, bottom_width)
    top_height = max((r[2] for r in top_row), default=0)
    bottom_height = max((r[2] for r in bottom_row), default=0)
    canvas_height_ft = top_height + bottom_height + corridor_width_ft + 2 * wall_thickness_ft

    img_w = int((canvas_width_ft + 2 * wall_thickness_ft) * scale) + 2 * margin
    img_h = int(canvas_height_ft * scale) + 2 * margin
    img = Image.new("RGB", (img_w, img_h), "white")
    draw = ImageDraw.Draw(img)

    offset_x = margin + int(wall_thickness_ft * scale)
    offset_y = margin + int(wall_thickness_ft * scale)

    def draw_rooms(rooms, y_start_ft):
        x_cursor_ft = 0.0
        for name, w_ft, h_ft in rooms:
            x1 = offset_x + int(x_cursor_ft * scale)
            y1 = offset_y + int(y_start_ft * scale)
            x2 = x1 + int(w_ft * scale)
            y2 = y1 + int(h_ft * scale)
            draw.rectangle([x1, y1, x2, y2], fill="#e6f2ff", outline="black", width=wall_px)
