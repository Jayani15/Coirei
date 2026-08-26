import { useState } from "react";

function Chat() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [listening, setListening] = useState(false);

  // Job description states
  const [file, setFile] = useState(null);
  const [jobId, setJobId] = useState(null);
  const [uploading, setUploading] = useState(false);

  const logout = () => {
    localStorage.removeItem("user_id");
    localStorage.removeItem("username");

    window.location.reload();
  };


  // =========================
  // Upload Job Description
  // =========================

  const uploadJob = async () => {
    if (!file) {
      alert("Please select a job description first.");
      return;
    }

    setUploading(true);

    try {
      const formData = new FormData();

      formData.append("file", file);

      const response = await fetch(
        "http://127.0.0.1:8000/upload-job",
        {
          method: "POST",
          body: formData
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
          data.error ||
          "Upload failed"
        );
      }

      setJobId(data.job_id);

      alert(
        `Job description uploaded successfully!\n${data.chunks} chunks created.`
      );

    } catch (error) {

      console.error("Upload error:", error);

      alert(
        "Upload failed: " + error.message
      );

    } finally {
      setUploading(false);
    }
  };


  // =========================
  // Send Chat Message
  // =========================

  const sendMessage = async () => {

    if (!message.trim() || loading) {
      return;
    }

    const userMessage = message;

    // Show user's message immediately
    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: userMessage
      }
    ]);

    setMessage("");
    setLoading(true);

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            message: userMessage,
            user_id: Number(localStorage.getItem("user_id")),
            job_id: jobId
          })
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
          `Server error: ${response.status}`
        );
      }

      // Show AI response
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.response
        }
      ]);

      const speech = new SpeechSynthesisUtterance(
        data.response
      );

    speech.lang = "en-US";

    window.speechSynthesis.speak(speech);

    } catch (error) {

      console.error("Chat error:", error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Sorry, something went wrong: " + error.message
        }
      ]);

    } finally {
      setLoading(false);
    }
  };

  const startVoiceInput = () => {

        const SpeechRecognition =
      window.SpeechRecognition ||
      window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Speech recognition is not supported in this browser.");
      return;
    }

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => {
      setListening(true);
    };

    recognition.onresult = (event) => {

      const transcript =
        event.results[0][0].transcript;

      setMessage(transcript);
    };

    recognition.onerror = (event) => {

      console.error(
        "Speech recognition error:",
        event.error
      );

      alert("Could not understand your voice.");
    };

    recognition.onend = () => {
      setListening(false);
    };

    recognition.start();
  };


  return (
    <div>

      <h1>AI Job Assistant</h1>

      <button onClick={logout}>
        Logout
      </button>


      {/* =========================
          JOB DESCRIPTION UPLOAD
          ========================= */}

      <div>

        <h3>Job Description</h3>

        <input
          type="file"
          accept=".pdf,.docx,.txt"
          onChange={(e) => {
            setFile(e.target.files[0]);
          }}
        />

        <button
          onClick={uploadJob}
          disabled={uploading || !file}
        >
          {uploading
            ? "Uploading..."
            : "Upload Job"}
        </button>

        {jobId && (
          <p>
            ✅ Job description uploaded
          </p>
        )}

      </div>


      {/* =========================
          CHAT MESSAGES
          ========================= */}

      <div>

        {messages.map((msg, index) => (

          <div key={index}>

            <strong>
              {msg.role === "user"
                ? "You"
                : "AI"}:
            </strong>

            <span>
              {" "}{msg.content}
            </span>

          </div>

        ))}

        {loading && (
          <p>AI is thinking...</p>
        )}

      </div>


      {/* =========================
          CHAT INPUT
          ========================= */}

      <div>

        <input
            type="text"
            value={message}
            placeholder="Ask about the job..."
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => {
                if (e.key === "Enter") {
                sendMessage();
                }
            }}
        />

        <button
            onClick={startVoiceInput}
            disabled={listening}
        >
            {listening ? "🎙️ Listening..." : "🎤"}
        </button>

        <button
            onClick={sendMessage}
            disabled={loading}
        >
            {loading ? "Thinking..." : "Send"}
        </button>

      </div>

    </div>
  );
}

export default Chat;

