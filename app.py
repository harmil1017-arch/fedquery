import html
import os
import streamlit as st
from fedquery import answer

st.set_page_config(
    page_title="FedQuery | FOMC Intelligence",
    page_icon="🏛️",
    layout="wide",
)

# Load Streamlit Cloud secrets when deployed.
try:
    if "OPENAI_API_KEY" in st.secrets:
        os.environ.setdefault("OPENAI_API_KEY", st.secrets["OPENAI_API_KEY"])
    if "OPENAI_MODEL" in st.secrets:
        os.environ.setdefault("OPENAI_MODEL", st.secrets["OPENAI_MODEL"])
except Exception:
    pass

st.markdown("""
<style>
    .stApp {
        background-color: #071521;
        color: #f4f7fb;
    }

    .hero {
        padding: 2rem 2.2rem;
        border: 1px solid #24445d;
        border-radius: 20px;
        background: linear-gradient(120deg, #0b2235, #103d4b);
        margin-bottom: 1.5rem;
    }

    .badge {
        color: #8be1c8;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.08em;
    }

    .hero h1 {
        font-size: 3rem;
        margin: 0.3rem 0;
    }

    .hero p {
        color: #c3d2dc;
        font-size: 1.05rem;
        margin-bottom: 0;
    }

    .metric-card {
        background: #0d2232;
        border: 1px solid #24445d;
        border-radius: 14px;
        padding: 1rem;
        text-align: center;
    }

    .metric-card h3 {
        color: #8be1c8;
        font-size: 1.4rem;
        margin: 0;
    }

    .metric-card p {
        color: #b7c6cf;
        font-size: 0.85rem;
        margin: 0.25rem 0 0;
    }

    .answer-box {
        background: #0d2939;
        border-left: 5px solid #6de0b6;
        border-radius: 12px;
        padding: 1.3rem;
        font-size: 1.08rem;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

if "question" not in st.session_state:
    st.session_state.question = ""

st.markdown("""
<div class="hero">
    <div class="badge">FOMC RESEARCH ASSISTANT</div>
    <h1>FedQuery</h1>
    <p>Ask questions about Federal Reserve statements. Answers are grounded only in retrieved FOMC passages and include citations.</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        '<div class="metric-card"><h3>6</h3><p>FOMC statements</p></div>',
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        '<div class="metric-card"><h3>31</h3><p>Indexed paragraphs</p></div>',
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        '<div class="metric-card"><h3>Top 4</h3><p>Retrieved passages</p></div>',
        unsafe_allow_html=True,
    )

st.write("")
st.subheader("Ask FedQuery")
st.caption("Choose an example or enter your own question.")

examples = [
    ("Target range", "What target range did the Committee set on September 16, 2026?"),
    ("Economic outlook", "How did the Committee describe economic activity?"),
    ("Inflation", "What did the statement say about inflation?"),
]

example_columns = st.columns(3)

for column, (label, example_question) in zip(example_columns, examples):
    if column.button(label, use_container_width=True):
        st.session_state.question = example_question

with st.form("question_form"):
    user_question = st.text_input(
        "Your question",
        key="question",
        placeholder="Example: What did the Committee say about inflation?",
    )

    submitted = st.form_submit_button(
        "Search FOMC statements",
        use_container_width=True,
    )

if submitted and user_question.strip():
    with st.spinner("Retrieving the most relevant FOMC passages..."):
        try:
            result = answer(user_question.strip())

            response = result.get("answer", "Not found in the documents.")
            passages = result.get("passages", [])

            st.subheader("Answer")
            safe_response = html.escape(str(response))
            st.markdown(
                f'<div class="answer-box">{safe_response}</div>',
                unsafe_allow_html=True,
            )

            st.write("")
            st.subheader("Retrieved passages")

            if passages:
                for i, passage in enumerate(passages, start=1):
                    title = f"Retrieved passage {i}"
                    text = passage

                    if isinstance(passage, dict):
                        metadata = passage.get("metadata", {})
                        date = metadata.get("date")
                        paragraph = metadata.get("paragraph")

                        if date and paragraph:
                            title = f"{date} · Paragraph {paragraph}"
                        elif date:
                            title = str(date)

                        text = (
                            passage.get("text")
                            or passage.get("document")
                            or str(passage)
                        )

                    with st.expander(title):
                        st.write(text)
            else:
                st.info("No retrieved passages were returned.")

        except Exception as error:
            st.error(f"Could not answer the question: {error}")

with st.sidebar:
    st.header("About FedQuery")
    st.write(
        "A retrieval-augmented Q&A app built over six Federal Open Market Committee statements."
    )

    st.divider()

    st.subheader("How it works")
    st.write("1. Your question is embedded.")
    st.write("2. ChromaDB retrieves relevant paragraphs.")
    st.write("3. The LLM answers only from those passages.")
    st.write("4. Supporting passages are shown below.")

    st.divider()

    st.caption("For research and educational use only. Not financial advice.")