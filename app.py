import streamlit as st
import json
from layout_engine import generate_layout_image
from utils import parse_prompt

# Streamlit UI
st.set_page_config(page_title="AI Floor Plan Generator", layout="centered")
st.title("🧠 AI Floor Plan Generator")
st.write("Describe your space and we'll generate a basic schematic layout.")

# Prompt Input
user_prompt = st.text_area("✍️ Describe your space:", 
                           placeholder="e.g. A radiology clinic with 4 exam rooms, a waiting area, 2 staff offices, and a pantry")

if st.button("Generate Floor Plan"):
    if not user_prompt.strip():
        st.warning("Please enter a description.")
    else:
        st.info("Processing prompt and generating layout...")
        try:
            room_list = parse_prompt(user_prompt)
            image = generate_layout_image(room_list)
            st.image(image, caption="AI-generated schematic floor plan", use_container_width=True)
            st.success("✅ Done!")
        except Exception as e:
            st.error(f"Something went wrong: {e}")

st.title("🧠 AI Floor Plan Generator - REVISION 1")
