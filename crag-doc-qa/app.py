import streamlit as st
import tempfile
import os

from rag import (
    index_documents,
    ask_question
)

# -----------------------------
# Streamlit Configuration
# -----------------------------
st.set_page_config(
    page_title="CRAG Document Q&A",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Corrective RAG (CRAG) Document Q&A")
st.write("Upload a document and ask questions based on its content.")

# -----------------------------
# Session State
# -----------------------------
if "indexed" not in st.session_state:
    st.session_state.indexed = False

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.header("Upload Document")

    uploaded_file = st.file_uploader(
        "Choose a PDF or DOCX",
        type=["pdf", "docx"]
    )

    if uploaded_file:

        if st.button("Index Document"):

            with st.spinner("Indexing document..."):

                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=os.path.splitext(uploaded_file.name)[1]
                ) as tmp:

                    tmp.write(uploaded_file.read())
                    temp_path = tmp.name

                try:
                    index_documents(temp_path)

                    st.session_state.indexed = True
                    st.success("Document Indexed Successfully!")

                except Exception as e:
                    st.error(str(e))

                finally:
                    os.remove(temp_path)

# -----------------------------
# Main Chat Interface
# -----------------------------
if st.session_state.indexed:

    st.subheader("Ask Questions")

    question = st.text_input(
        "Enter your question"
    )

    if st.button("Generate Answer"):

        if question.strip() == "":
            st.warning("Please enter a question.")

        else:

            with st.spinner("Generating Answer..."):

                answer, retrieved_chunks = ask_question(question)

            st.markdown("## Answer")

            st.write(answer)

            with st.expander("Retrieved Context"):

                for i, chunk in enumerate(retrieved_chunks, start=1):

                    st.markdown(f"### Chunk {i}")

                    st.write(chunk)

                    st.divider()

else:

    st.info("Please upload and index a document first.")