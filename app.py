import streamlit as st
from claude_service import ClaudeService
from database import init_db, save_bread, get_all_breads
from datetime import datetime

if 'db_initialized' not in st.session_state:
    init_db()
    st.session_state.db_initialized = True

if "claude" not in st.session_state:
    st.session_state.claude = ClaudeService()

claude = st.session_state.claude    

st.set_page_config(
    page_title="Sourdough Journal",
    layout="wide"
)

st.title("Sourdough Journal")


with st.sidebar:
    st.header("Navigation")
    page = st.radio("Go to:", ["New Bake", "Past Breads", "Stats"])


if page == "New Bake":
    st.header("Log a New Bake")

    photo = st.file_uploader("Upload phhoto:", type=['jpg', 'png'])

    if photo:
        st.image(photo, caption="Your bread", width=400)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{photo.name}"

    notes = st.text_area("Notes: ", height=150)

    if st.button("Analyze", disabled=(photo is None)):
        with st.spinner("Claude is analyzing..."):
            with open(f"uploads/{photo.name}", "wb") as f:
                f.write(photo.getvalue())
                photo.seek(0)
                
            result = ""

            def stream_and_capture(generator):
                global result
                for chunk in generator:
                    result += chunk
                    yield chunk

            stream = claude.analyze_bread(photo, notes)
            st.write_stream(stream_and_capture(stream))

            save_bread(notes, result, photo.name)
            st.success("Analysis complete!")

elif page == "Past Breads":
    st.header("Past Breads")
    breads = get_all_breads()
    for bread in breads:
        date_obj = datetime.fromisoformat(bread["date"])
        formatted_date = date_obj.strftime("%d.%m.%Y")
        st.subheader(formatted_date)

        st.write(f"Notes: {bread['notes']}")
        st.image(bread["image_url"], caption="Your bread", width=400)
        st.write(f"Feedback: {bread['feedback']}")
        st.write("---")
        
        


elif page == "Stats":
    st.header("Your Stats")
    st.write("Analytics coming soon!")
    
