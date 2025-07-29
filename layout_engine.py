from PIL import Image, ImageDraw, ImageFont

# Load a default font (this prevents the 'NoneType' error)
font = ImageFont.load_default()

# Constants
SCALE = 10  # 1 foot = 10 pixels
WALL_THICKNESS_FT = 0.5
CORRIDOR_WIDTH_FT = 6.0
MARGIN_PX = 20

# Default sizes in feet (width, depth)
DEFAULT_ROOM_SIZES = {
    "exam room": (10.0, 13.0),
    "waiting area": (12.0, 12.0),
    "cafe": (15.0, 15.0),
    "lobby": (18.0, 18.0),
    "staff open office": (20.0, 15.0),
    "pantry": (10.0, 10.0)
}


def generate_layout_image(room_list):
    """
    Draws a simple 2-row floor plan with a horizontal corridor in the middle.
    """
    # Divide into top and bottom rows (split evenly)
    half = len(room_list) // 2
    top_rooms = room_list[:half]
    bottom_rooms = room_list[half:]

    top_depth = max(room["depth"] for room in top_rooms) if top_rooms else 0
    bottom_depth = max(room["depth"] for room in bottom_rooms) if bottom_rooms else 0
    corridor_length = max(sum(room["width"] for room in top_rooms),
                          sum(room["width"] for room in bottom_rooms))

    # Compute overall image size
    wall_px = int(WALL_THICKNESS_FT * SCALE)
    interior_width = corridor_length
    interior_height = top_depth + CORRIDOR_WIDTH_FT + bottom_depth

    img_w = int((interior_width + 2 * WALL_THICKNESS_FT) * SCALE) + 2 * MARGIN_PX
    img_h = int((interior_height + 2 * WALL_THICKNESS_FT) * SCALE) + 2 * MARGIN_PX

    img = Image.new("RGB", (img_w, img_h), "white")
    draw = ImageDraw.Draw(img)

    offset_x = MARGIN_PX + int(WALL_THICKNESS_FT * SCALE)
    offset_y = MARGIN_PX + int(WALL_THICKNESS_FT * SCALE)

    # Draw function for each row
    def draw_row(rooms, y_start_ft):
        x_cursor_ft = 0.0
        for room in rooms:
            x1 = offset_x + int(x_cursor_ft * SCALE)
            y1 = offset_y + int(y_start_ft * SCALE)
            x2 = x1 + int(room["width"] * SCALE)
            y2 = y1 + int(room["depth"] * SCALE)

            draw.rectangle([x1, y1, x2, y2], fill="#e6f2ff", outline="black", width=wall_px)
            draw.text((x1 + 5, y1 + 5), room["name"], fill="black", font=font)

            x_cursor_ft += room["width"]

    # Draw top rooms, corridor, bottom rooms
    draw_row(top_rooms, 0)
    draw_row(bottom_rooms, top_depth + CORRIDOR_WIDTH_FT)

    # Draw corridor
    cx1 = offset_x
    cx2 = offset_x + int(corridor_length * SCALE)
    cy1 = offset_y + int(top_depth * SCALE)
    cy2 = cy1 + int(CORRIDOR_WIDTH_FT * SCALE)
    draw.rectangle([cx1, cy1, cx2, cy2], fill="lightgray")

    return img
