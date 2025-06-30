import React, { useState } from "react";
import axios from "axios";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question) return;

    setLoading(true);
    setAnswer("");

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/", // <-- your ngrok URL here
        { question }
      );
      setAnswer(response.data.answer);
    } catch (error) {
      setAnswer("Error: Unable to get response.");
      console.error(error);
    }

    setLoading(false);
  };

  return (
    <div
      style={{
        maxWidth: 600,
        margin: "2rem auto",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <h1>HR Assistant</h1>
      <input
        type="text"
        placeholder="Ask your HR question here..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        style={{ width: "100%", padding: "0.75rem", fontSize: "1rem" }}
      />
      <button
        onClick={askQuestion}
        disabled={loading}
        style={{
          marginTop: "1rem",
          padding: "0.75rem 1.5rem",
          fontSize: "1rem",
          cursor: "pointer",
        }}
      >
        {loading ? "Thinking..." : "Ask"}
      </button>

      {answer && (
        <div
          style={{
            marginTop: "2rem",
            padding: "1rem",
            border: "1px solid #ddd",
            borderRadius: "8px",
            backgroundColor: "#000000",
            whiteSpace: "pre-wrap",
          }}
        >
          <strong>Answer:</strong>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}

export default App;
// This code is a simple React application that allows users to ask HR-related questions.
// It uses Axios to send the question to a backend server (which you need to set up).
