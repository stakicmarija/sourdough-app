import base64

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

# initialize chat history
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []



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

            image_bytes = base64.standard_b64encode(photo.getvalue()).decode("utf-8")

            st.session_state.chat_messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": photo.type, 
                                "data": image_bytes,
                            },
                        },
                        {
                            "type": "text",
                            "text": notes,
                        },
                    ],
                }
            ]

            result = ""

            def stream_and_capture(generator):
                global result  
                for chunk in generator:
                    result += chunk
                    yield chunk

            stream = claude.chat(st.session_state.chat_messages)

            st.write_stream(stream_and_capture(stream))

            # save to db
            save_bread(notes, result, filename)

            st.success("Analysis complete!")
            st.session_state.chat_messages.append({"role": "assistant", "content": result})

    if len(st.session_state.chat_messages) >= 2:
        st.header("Chat about your bread")

        # display chat messages from history on app rerun
        for i in range(2, len(st.session_state.chat_messages)):
            with st.chat_message(st.session_state.chat_messages[i]["role"]):
                st.markdown(st.session_state.chat_messages[i]["content"])

        if prompt := st.chat_input("Ask something about your bread"):
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                stream = claude.chat(st.session_state.chat_messages)
                message_placeholder = st.empty()
                full_response = ""
                for response in stream:
                    full_response += response
                    message_placeholder.markdown(full_response)
                st.session_state.chat_messages.append({"role": "assistant", "content": full_response})
           
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