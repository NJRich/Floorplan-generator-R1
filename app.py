import streamlit as st
from utils import parse_prompt
from layout_engine import generate_layout_image

st.set_page_config(page_title="AI Floor Plan Generator", layout="centered")

# App title and description
st.markdown("🎨 **AI Floor Plan Generator - REVISION 1**")
st.write("Describe your space and we'll generate a basic schematic layout.")

# Input prompt
user_input = st.text_area("📝 Describe your space:", placeholder="e.g. a hospital with 2 procedure rooms, a lobby and 4 patient rooms")

uploaded_file = st.file_uploader("📐 Upload floor outline (PNG only)", type=["png"])
outline_bbox = None

if uploaded_file:
    from layout_engine import extract_outline_bbox
    outline_bbox = extract_outline_bbox(uploaded_file)
    st.success(f"Detected floor outline boundary: {outline_bbox} ft")

# Button to generate layout
if st.button("Generate Floor Plan"):
    if not user_input.strip():
        st.warning("Please enter a description of your space.")
    else:
        st.info("Processing prompt and generating layout...")

        try:
            parsed_rooms = parse_prompt(user_input)
            st.write("🧾 Parsed room dictionary:", parsed_rooms)  # Debug output

            if not parsed_rooms:
                st.error("No valid rooms were parsed from your prompt. Please make sure the room names match what's in the database.")
            else:
                image = generate_layout_image(parsed_rooms)

                if image:
                    st.success("✅ Floor plan generated!")
                    st.image(image, caption="Generated Floor Plan", use_container_width=True)
                else:
                    st.error("Something went wrong — no image was generated.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
