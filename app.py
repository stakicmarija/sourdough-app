import streamlit as st
from claude_service import ClaudeService


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

    notes = st.text_area("Notes: ", height=150)

    claude = ClaudeService()

    if st.button("Analyze"):
        with st.spinner("Claude is analyzing..."):
            result = claude.analyze_bread(photo, notes)
            st.write(result)
            st.success("Analysis complete!")

elif page == "Past Bakes":
    st.header("Past Bakes")

elif page == "Stats":
    st.header("Your Stats")
    st.write("Analytics coming soon!")
    
