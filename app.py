import streamlit as st
from claude_service import ClaudeService
from database import init_db, save_bread, get_all_breads
from datetime import datetime

# init DB
if 'db_initialized' not in st.session_state:
    init_db()
    st.session_state.db_initialized = True

# Claude instance
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


# =========================
# NEW BAKE
# =========================
if page == "New Bake":
    st.header("Log a New Bake")

    photo = st.file_uploader("Upload photo:", type=['jpg', 'png'])

    filename = None

    if photo:
        st.image(photo, caption="Your bread", width=400)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{photo.name}"

    notes = st.text_area("Notes:", height=150)

    if st.button("Analyze", disabled=(photo is None)):
        with st.spinner("Claude is analyzing..."):

            # save photo
            with open(f"uploads/{filename}", "wb") as f:
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

            # sačuvaj u bazu
            save_bread(notes, result, filename)

            st.success("Analysis complete!")


# =========================
# PAST BREADS
# =========================
elif page == "Past Breads":
    st.header("Past Breads")

    breads = get_all_breads()

    for bread in breads:
        date_obj = datetime.fromisoformat(bread["date"])
        formatted_date = date_obj.strftime("%d.%m.%Y")

        st.subheader(formatted_date)
        st.write(f"Notes: {bread['notes']}")
        st.image(bread["image_url"], width=400)
        st.write(f"Feedback: {bread['feedback']}")
        st.write("---")


# =========================
# STATS
# =========================
elif page == "Stats":
    st.header("Your Stats")
    st.write("Analytics coming soon!")