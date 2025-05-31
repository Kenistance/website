import React, { useState, useEffect } from 'react';
import '../styles/ChatBox.css';

function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);  // NEW

  const sessionId = "6d6e6c01-a728-4cd9-9ef3-94fe80e52632";

  useEffect(() => {
    async function fetchChatHistory() {
      try {
        const response = await fetch(`https://website3-ho1y.onrender.com/api/chat/chat-history/${sessionId}/`);
        const data = await response.json();
        setMessages(data.chat_history || []);
      } catch (error) {
        console.error("Error fetching chat history:", error);
      }
    }
    if (isOpen) fetchChatHistory();
  }, [sessionId, isOpen]);

  const sendMessage = async () => {
    const trimmed = input.trim();
    if (!trimmed) return;

    setMessages(prev => [...prev, { sender: "You", text: trimmed }]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch("https://website3-ho1y.onrender.com/api/chat/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: trimmed, session_id: sessionId })
      });

      const data = await response.json();
      const botReply = data.response || "Sorry, I didn't get that.";
      setMessages(prev => [...prev, { sender: "Bot", text: botReply }]);
    } catch (err) {
      console.error("Error sending message:", err);
      setMessages(prev => [...prev, { sender: "Bot", text: "⚠️ Could not connect to server." }]);
    }

    setLoading(false);
  };

  return (
    <div className="chatbox-wrapper-fixed">
      <button className="chatbox-toggle" onClick={() => setIsOpen(!isOpen)}>
        💬 {isOpen ? "Close Chat" : "Open Chat"}
      </button>

      {isOpen && (
        <div className={`chatbox-container ${isExpanded ? 'expanded' : ''}`}>
          <div className="chatbox-header">
            Chat With Me
            <button
              className="chatbox-expand-toggle"
              onClick={() => setIsExpanded(prev => !prev)}
              style={{ float: "right" }}
            >
              {isExpanded ? "⇩ Collapse" : "⇧ Expand"}
            </button>
          </div>

          <div className="chatbox-messages">
            {messages
              .filter(msg => msg.text && msg.text.trim() !== "")
              .map((msg, i) => {
                const sender = (msg.sender || "bot").toLowerCase();
                return (
                  <div key={i} className={`chatbox-message ${sender}`}>
                    <div className={`chatbox-bubble ${sender}`}>
                      {msg.text}
                    </div>
                  </div>
                );
              })}
          </div>

          <div className="chatbox-input-area">
            <input
              value={input}
              onChange={e => setInput(e.target.value)}
              className="chatbox-input"
              placeholder="Type a message..."
              onKeyDown={e => { if (e.key === 'Enter') sendMessage(); }}
            />
            <button
              onClick={sendMessage}
              className="chatbox-button"
              disabled={loading}
            >
              {loading ? "..." : "Send"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default ChatBox;
