import React, { useState, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";
import "./App.css";

export default function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: input }),
      });

      const data = await response.json();
      const botMessage = {
        sender: "bot",
        text: data.response || "⚠️ Không nhận được phản hồi từ máy chủ.",
        chunks: data.sample_chunks || "",
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "⚠️ Lỗi khi kết nối với server.", chunks: "" },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  // auto-scroll to bottom when new message added
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="app-container">
      <div className="chat-container">
        <header className="chat-header">
          <h2>StudyBuddy</h2>
          <p className="subtitle">
            A Vietnamese-friendly RAG-based teaching assistant 🤖
          </p>
          <p className="subtitle">💡 Tip: Ask me to explain, summarize, or calculate!</p>
        </header>

        <div className="chat-box">
          {messages.map((msg, i) => (
            <div key={i} className={`message ${msg.sender}`}>
              {msg.sender === "bot" ? (
                <>
                  <div className="markdown">
                    <ReactMarkdown
                      remarkPlugins={[remarkMath]}
                      rehypePlugins={[rehypeKatex]}
                    >
                      {msg.text}
                    </ReactMarkdown>
                  </div>

                  {msg.chunks && (
                    <details className="chunk-box">
                      <summary>📚 Relevant Chunks</summary>
                      <div className="chunk-markdown">
                        <ReactMarkdown
                          remarkPlugins={[remarkMath]}
                          rehypePlugins={[rehypeKatex]}
                        >
                          {msg.chunks}
                        </ReactMarkdown>
                      </div>
                    </details>
                  )}
                </>
              ) : (
                <div className="user-text">{msg.text}</div>
              )}
            </div>
          ))}

          {loading && (
            <div className="message bot loading-msg">⏳ em đang nghĩ... đợi chút ạ</div>
          )}
          <div ref={chatEndRef} />
        </div>

        <div className="input-area">
          <input
            className="chat-input"
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Hỏi tớ i :>"
            onKeyDown={handleKeyPress}
          />
          <button className="send-btn" onClick={sendMessage}>
            Gửi
          </button>
        </div>
      </div>
    </div>
  );
}
