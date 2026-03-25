import streamlit as st

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

    if st.button("Analyze"):
        with st.spinner("Claude is analyzing..."):
            st.success("Analysis complete!")

elif page == "Past Bakes":
    st.header("Past Bakes")

elif page == "Stats":
    st.header("Your Stats")
    st.write("Analytics coming soon!")
    
