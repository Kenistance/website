import React, { useState } from 'react';

function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    const trimmed = input.trim();
    if (!trimmed) return;

    // Add user's message to the chat box
    setMessages(prev => [...prev, { sender: "You", text: trimmed }]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/chat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: trimmed }) // sending just the message text
      });

      const data = await response.json();

      // Check if the response from the server contains the bot's message
      if (data.response) {
        setMessages(prev => [...prev, { sender: "Bot", text: data.response }]);
      } else {
        setMessages(prev => [...prev, { sender: "Bot", text: "No response received." }]);
      }
    } catch (err) {
      setMessages(prev => [...prev, { sender: "Bot", text: "⚠️ Could not connect to server." }]);
    }

    setLoading(false);
  };

  return (
    <div className="fixed bottom-4 right-4 w-80 bg-white border shadow rounded p-4 z-50">
      <h3 className="text-lg font-bold mb-2">💬 Chat With Me</h3>
      <div className="h-48 overflow-y-auto border p-2 mb-2 rounded bg-gray-50 text-sm">
        {messages.map((msg, i) => (
          <div key={i} className="mb-1">
            <strong className={msg.sender === "You" ? "text-blue-600" : "text-green-600"}>
              {msg.sender}:
            </strong> {msg.text}
          </div>
        ))}
      </div>
      <div className="flex gap-2">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          className="flex-1 border p-2 rounded"
          placeholder="Type a message..."
        />
        <button
          onClick={sendMessage}
          className="bg-blue-600 text-white px-3 rounded disabled:opacity-50"
          disabled={loading}
        >
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default ChatBox;
