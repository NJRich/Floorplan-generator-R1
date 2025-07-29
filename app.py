import streamlit as st
from layout_engine import generate_floorplan_image

# Streamlit setup
st.set_page_config(page_title="AI Floor Plan Generator", layout="centered")
st.title("🧠 AI Floor Plan Generator")
st.write("Describe your space and we’ll generate a basic layout.")

# Prompt input
prompt = st.text_area("✍️ Describe your space:", placeholder="e.g. A clinic with 3 exam rooms and a waiting area")

# Generate button
if st.button("Generate Floor Plan"):
    if not prompt.strip():
        st.warning("Please enter a space description.")
    else:
        st.info("Generating floor plan...")
        image = generate_floorplan_image(prompt)
        if image:
            st.success("✅ Floor plan generated!")
            st.image(image, caption="Auto-generated floor plan", use_container_width=True)
            st.markdown(f"**Prompt:** {prompt}")
        else:
            st.error("Sorry, we couldn’t recognize any rooms from your prompt.")
