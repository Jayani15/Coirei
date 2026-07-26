import streamlit as st

from retrieval import retrieve
from llm import ask_llm
from evaluator import evaluate_context, refine_context
from web_search import web_search
from stt import record_audio, speech_to_text
from tts import speak

st.set_page_config(page_title="Enterprise Customer Support Voice RAG")

st.title("🎙️ Enterprise Customer Support Voice RAG")

# Store question across reruns
if "question" not in st.session_state:
    st.session_state.question = ""

# Voice Input
if st.button("🎤 Speak"):

    with st.spinner("Listening..."):

        audio = record_audio(duration=5)

        st.session_state.question = speech_to_text(audio)

    st.success("Voice captured successfully!")

# Show the recognized question
st.text_area(
    "Recognized Question",
    value=st.session_state.question,
    height=80
)

# Allow user to edit it if Whisper made a mistake
st.session_state.question = st.text_input(
    "Edit Question (optional)",
    value=st.session_state.question
)

# Submit
if st.button("Submit"):

    question = st.session_state.question.strip()

    if question == "":
        st.warning("Please speak or type a question.")
        st.stop()

    # Retrieval
    results = retrieve(question)

    local_context = ""
    local_sources = []

    for r in results:
        local_context += r.payload["text"] + "\n\n"
        local_sources.append(r.payload["source"])

    evaluation = evaluate_context(results)

    status = evaluation["status"]

    if status == "Correct":
        st.success("🟢 Retrieval Status: Correct")

    elif status == "Ambiguous":
        st.warning("🟡 Retrieval Status: Ambiguous")

    else:
        st.error("🔴 Retrieval Status: Incorrect")

    st.write("### Retrieval Scores")

    for r in results:
        st.write(f"{r.payload['source']} → {r.score:.3f}")

    # CRAG
    if status == "Correct":

        final_context = local_context
        final_sources = local_sources

    elif status == "Ambiguous":

        refined_context = refine_context(
            question,
            local_context
        )

        web_context, web_sources = web_search(question)

        final_context = f"""
COMPANY KNOWLEDGE

{refined_context}

-----------------------------------

WEB KNOWLEDGE

{web_context}
"""

        final_sources = local_sources + web_sources

    else:

        web_context, web_sources = web_search(question)

        final_context = web_context

        final_sources = web_sources

    # LLM
    answer = ask_llm(question, final_context)

    st.write("## 🤖 Answer")
    st.write(answer)

    # Voice Output
    speak(answer)

    # Sources
    st.write("## 📚 Sources")

    for source in final_sources:
        st.write("-", source)