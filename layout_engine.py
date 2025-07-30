import cv2
import numpy as np

def extract_outline_bbox(uploaded_file, dpi=96, scale=10):
    """
    Reads the uploaded PNG file and extracts the bounding box (in ft).
    Assumes black outline on white background.
    """
    # Convert uploaded_file to OpenCV image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)

    _, thresh = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return None

    x, y, w, h = cv2.boundingRect(contours[0])
    
    # Convert px to ft using DPI
    inches_w = w / dpi
    inches_h = h / dpi
    ft_w = round(inches_w / 12, 1)
    ft_h = round(inches_h / 12, 1)

    return (ft_w, ft_h)  # width_ft, height_ft

import json
from PIL import Image, ImageDraw
import math

# Load the room database
with open("room_database.json", "r") as f:
    ROOM_DATABASE = json.load(f)

def estimate_size_ft(room_data):
    """
    Estimate room size in (width, height) feet from recommended_size_sqft.
    Assumes square room for simplicity.
    """
    sqft = room_data.get("recommended_size_sqft", 100)
    side = math.sqrt(sqft)
    return round(side, 1), round(side, 1)

def generate_layout_image(parsed_rooms, scale=10, wall_thickness_ft=0.5, corridor_width_ft=6.0):
    """
    Takes parsed_rooms as a dictionary and returns a Pillow image with a basic floor plan.
    parsed_rooms should look like: {'lobby': 1, 'procedure room': 2}
    """
    wall_px = int(wall_thickness_ft * scale)
    margin = 20

    room_list = []
    for room_type, count in parsed_rooms.items():
        if not isinstance(count, int) or count <= 0:
            continue  # Skip invalid counts

        if room_type in ROOM_DATABASE:
            room_info = ROOM_DATABASE[room_type]

            # Use size_ft if available; else estimate
            if "size_ft" in room_info:
                width, height = room_info["size_ft"]
            else:
                width, height = estimate_size_ft(room_info)

            # Use 'name' if defined, otherwise fallback to room_type
            room_name = room_info.get("name", room_type)

            for i in range(count):
                label = f"{room_name} {i+1}" if count > 1 else room_name
                room_list.append((label, width, height))
        else:
            print(f"⚠️ Room type not found in database: {room_type}")

    if not room_list:
        print("❌ No valid rooms were added to the layout.")
        return None

    # Split into two rows (top/bottom)
    mid = len(room_list) // 2
    top_row = room_list[:mid]
    bottom_row = room_list[mid:]

    # Calculate layout dimensions in feet
    top_width = sum(r[1] for r in top_row)
    bottom_width = sum(r[1] for r in bottom_row)
    canvas_width_ft = max(top_width, bottom_width)
    top_height = max((r[2] for r in top_row), default=0)
    bottom_height = max((r[2] for r in bottom_row), default=0)
    canvas_height_ft = top_height + bottom_height + corridor_width_ft + 2 * wall_thickness_ft

    # Convert to pixel dimensions
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
            draw.text((x1 + 5, y1 + 5), name, fill="black")
            x_cursor_ft += w_ft

    # Draw both rows
    draw_rooms(top_row, 0)
    draw_rooms(bottom_row, top_height + corridor_width_ft)

    return img
