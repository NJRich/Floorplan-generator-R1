import streamlit as st
from utils import parse_prompt
from layout_engine import generate_layout_image

st.set_page_config(page_title="AI Floor Plan Generator", layout="centered")

# App title and description
st.markdown("🎨 **AI Floor Plan Generator - REVISION 1**")
st.write("Describe your space and we'll generate a basic schematic layout.")

# Input prompt
user_input = st.text_area("📝 Describe your space:", placeholder="e.g. a hospital with 2 procedure rooms, a lobby and 4 patient rooms")

# Button to generate layout
if st.button("Generate Floor Plan"):
    if not user_input.strip():
        st.warning("Please enter a description of your space.")
    else:
        st.info("Processing prompt and generating layout...")
        try:
            parsed_rooms = parse_prompt(user_input)
            image = generate_layout_image(parsed_rooms)

            if image:
                st.success("✅ Floor plan generated!")
                st.image(image, caption="Generated Floor Plan", use_column_width=True)
            else:
                st.error("Something went wrong — no image was generated. Please check if the room types in your prompt exist in the database.")
        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")
