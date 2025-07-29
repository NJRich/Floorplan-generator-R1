from PIL import Image, ImageDraw

def generate_layout_image(room_data):
    """
    Generate a simple 2-row floor plan with corridor in between.
    Accepts a list of room dictionaries, each with name, width, and depth in feet.
    """
    scale = 10  # pixels per foot
    wall_thickness_ft = 0.5
    corridor_width_ft = 6.0
    wall_px = int(wall_thickness_ft * scale)
    margin = 20

    # Split rooms into top and bottom rows (roughly half each)
    mid = len(room_data) // 2
    top_rooms = room_data[:mid]
    bottom_rooms = room_data[mid:]

    top_depth = max(room["depth"] for room in top_rooms) if top_rooms else 0
    bottom_depth = max(room["depth"] for room in bottom_rooms) if bottom_rooms else 0
    corridor_length = max(
        sum(room["width"] for room in top_rooms),
        sum(room["width"] for room in bottom_rooms)
    )

    # Canvas dimensions
    interior_width = corridor_length
    interior_height = top_depth + corridor_width_ft + bottom_depth
    img_w = int((interior_width + 2 * wall_thickness_ft) * scale) + 2 * margin
    img_h = int((interior_height + 2 * wall_thickness_ft) * scale) + 2 * margin

    # Create blank canvas
    img = Image.new("RGB", (img_w, img_h), "white")
    draw = ImageDraw.Draw(img)

    offset_x = margin + wall_px
    offset_y = margin + wall_px

    def draw_rooms(rooms, y_start_ft):
        x_cursor = 0.0
        for room in rooms:
            x1 = offset_x + int(x_cursor * scale)
            y1 = offset_y + int(y_start_ft * scale)
            x2 = x1 + int(room["width"] * scale)
            y2 = y1 + int(room["depth"] * scale)

            # D
