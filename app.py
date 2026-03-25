import streamlit as st
from claude_service import ClaudeService
from database import init_db, save_bread
from datetime import datetime

init_db()

st.set_page_config(
    page_title="Sourdough Journal",
    layout="wide"
)

st.title("Sourdough Journal")


with st.sidebar:
    st.header("Navigation")
    page = st.radio("Go to:", ["New Bake", "Past Bakes", "Stats"])


if page == "New Bake":
    st.header("Log a New Bake")

    photo = st.file_uploader("Upload phhoto:", type=['jpg', 'png'])

    if photo:
        st.image(photo, caption="Your bread", width=400)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{photo.name}"

    notes = st.text_area("Notes: ", height=150)

    claude = ClaudeService()

    if st.button("Analyze", disabled=(photo is None)):
        with st.spinner("Claude is analyzing..."):
            with open(f"uploads/{photo.name}", "wb") as f:
                f.write(photo.getvalue())
                photo.seek(0)
            result = claude.analyze_bread(photo, notes)
            save_bread(notes, result, photo.name)
            st.write(result)
            st.success("Analysis complete!")

elif page == "Past Bakes":
    st.header("Past Bakes")

elif page == "Stats":
    st.header("Your Stats")
    st.write("Analytics coming soon!")
    
