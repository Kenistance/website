import React, { useState, useEffect } from 'react';
import '../styles/ChatBox.css';

function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const sessionId = "6d6e6c01-a728-4cd9-9ef3-94fe80e52632";

  useEffect(() => {
    async function fetchChatHistory() {
      try {
        const response = await fetch(`/api/chat/chat-history/${sessionId}/`);
        const data = await response.json();
        setMessages(data.chat_history);
      } catch (error) {
        console.error("Error fetching chat history", error);
      }
    }
    fetchChatHistory();
  }, [sessionId]);

  const generateBotReply = (userMessage) => {
    const message = userMessage.toLowerCase();
    if (message.includes("hello") || message.includes("hi")) {
      return "Hi there! How can I assist you today?";
    } else if (message.includes("services")) {
      return "I offer web development, data analytics, and task automation services.";
    } else if (message.includes("project")) {
      return "I’d love to help! What kind of project do you have in mind?";
    } else if (message.includes("price") || message.includes("cost")) {
      return "Pricing depends on the project details. Could you share more info?";
    } else if (message.includes("python")) {
      return "I specialize in Python for automation and backend development.";
    } else if (message.includes("thanks") || message.includes("thank you")) {
      return "You're welcome! Feel free to ask anything else.";
    } else {
      return "I'm still learning! Let me know if I can assist you with something else.";
    }
  };

  const sendMessage = async () => {
    const trimmed = input.trim();
    if (!trimmed) return;

    setMessages(prev => [...prev, { sender: "You", text: trimmed }]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/chat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: trimmed, session_id: sessionId })
      });

      const data = await response.json();
      const botReply = data.response || generateBotReply(trimmed);
      setMessages(prev => [...prev, { sender: "Bot", text: botReply }]);

    } catch (err) {
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
        <div className="chatbox-container">
          <div className="chatbox-header">Chat With Me</div>
          <div className="chatbox-messages">
            {messages.map((msg, i) => (
              <div key={i} className={`chatbox-message ${msg.sender.toLowerCase()}`}>
                <div className={`chatbox-bubble ${msg.sender.toLowerCase()}`}>{msg.text}</div>
              </div>
            ))}
          </div>
          <div className="chatbox-input-area">
            <input
              value={input}
              onChange={e => setInput(e.target.value)}
              className="chatbox-input"
              placeholder="Type a message..."
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
