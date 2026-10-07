import streamlit as st

from create_pipeline import run_research_pipeline


st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 Multi-Agent Research System")
st.write(
    "Search the web, read relevant sources, generate a research report, "
    "and critique the final report."
)

topic = st.text_area(
    "Enter your research topic",
    placeholder="Example: What is the impact of AI on software engineering?"
)

if st.button("Start Research", type="primary"):

    if not topic.strip():
        st.warning("Please enter a research topic.")

    else:

        with st.spinner("Running research pipeline..."):

            result = run_research_pipeline(topic)

        st.success("Research completed!")

        st.subheader("🔎 Search Results")
        st.write(result["search_results"])

        st.subheader("📖 Scraped Content")
        st.write(result["scraped_content"])

        st.subheader("📝 Research Report")
        st.write(result["report"])

        st.subheader("🔍 Critic Feedback")
        st.write(result["critique"])