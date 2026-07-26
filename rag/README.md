# 🎙️ Voice-Enabled Corrective Retrieval-Augmented Generation (CRAG)

An intelligent enterprise customer support chatbot that combines **Corrective Retrieval-Augmented Generation (CRAG)** with **Speech-to-Text (STT)** and **Text-to-Speech (TTS)** capabilities. The system accepts voice queries, retrieves the most relevant information from a knowledge base, evaluates the retrieved context, supplements it with web search when necessary, and responds with both text and speech.

---

## 🚀 Features

- 🎤 Voice-based user input
- 📝 Speech-to-Text using Faster-Whisper
- 📚 Vector-based document retrieval using Qdrant
- 🤖 Corrective RAG (CRAG) pipeline
- 🌐 Automatic web search for insufficient retrieval
- 🧠 LLM-powered response generation
- 🔊 Text-to-Speech response
- 📄 Source document citation
- 💻 Interactive Streamlit interface

---

## 🏗️ System Architecture

```
User Voice
     │
     ▼
Speech-to-Text (Whisper)
     │
     ▼
User Query
     │
     ▼
Vector Retrieval (Qdrant)
     │
     ▼
Context Evaluation
     │
 ┌───┴───────────────┐
 │                   │
Correct          Ambiguous/Incorrect
 │                   │
 ▼                   ▼
Local Context   Refine + Web Search
 │                   │
 └─────────┬─────────┘
           ▼
      Final Context
           ▼
      Large Language Model
           ▼
 Generated Response
           ▼
 Text-to-Speech
           ▼
 Spoken Response
```

---

## 📂 Project Structure

```
.
├── app.py                 # Streamlit application
├── retrieval.py           # Vector database retrieval
├── evaluator.py           # CRAG context evaluation
├── llm.py                 # LLM response generation
├── web_search.py          # Web search integration
├── stt.py                 # Speech-to-Text
├── tts.py                 # Text-to-Speech
├── ingest.py              # Document ingestion
├── requirements.txt
└── README.md
```

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Faster-Whisper
- Qdrant
- LangChain
- Groq LLM
- gTTS
- SoundDevice
- SciPy

---

## ▶️ Running the Application

```bash
streamlit run app.py
```

---

## 🎤 Usage

1. Launch the Streamlit application.
2. Click **🎤 Speak**.
3. Ask your question.
4. Click **Submit**.
5. The chatbot will:
   - Convert speech to text.
   - Retrieve relevant documents.
   - Evaluate retrieval quality using CRAG.
   - Perform web search if required.
   - Generate an AI response.
   - Read the response aloud.
   - Display supporting sources.

---

## 🧠 CRAG Workflow

### Correct Retrieval

- Uses retrieved documents directly.
- No web search performed.

### Ambiguous Retrieval

- Refines retrieved context.
- Performs web search.
- Combines both contexts.

### Incorrect Retrieval

- Ignores local retrieval.
- Answers entirely using web search.

---

## 📌 Sample Queries

- What is your return policy?
- How do I reset my password?
- Where are your offices located?
- Tell me about your premium subscription.
- What are today's AI news headlines?

---

## 📊 Output

The application displays:

- Recognized speech
- Retrieval status
- Similarity scores
- Generated answer
- Voice response
- Source documents
