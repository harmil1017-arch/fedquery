import os
import streamlit as st
from fedquery import answer

st.set_page_config(page_title="FedQuery", page_icon="🏦")
if "OPENAI_API_KEY" in st.secrets:
    os.environ.setdefault("OPENAI_API_KEY", st.secrets["OPENAI_API_KEY"])
if "OPENAI_MODEL" in st.secrets:
    os.environ.setdefault("OPENAI_MODEL", st.secrets["OPENAI_MODEL"])
st.title("FedQuery")
st.caption("Ask questions about six FOMC statements. Answers are grounded only in retrieved statements.")

question = st.text_input("Your question", placeholder="What was the target range on September 16, 2026?")
if question:
    try:
        with st.spinner("Searching statements…"):
            result = answer(question)
        st.subheader("Answer")
        st.write(result["answer"])
        with st.expander("Retrieved passages"):
            for p in result["passages"]:
                m = p["metadata"]
                st.markdown(f"**{m['meeting_date']} · paragraph {m['paragraph']}**")
                st.write(p["text"])
    except Exception as exc:
        st.error(f"Could not answer. Did you run ingest.py and configure OPENAI_API_KEY? ({exc})")
