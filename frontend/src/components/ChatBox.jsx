import React, { useState, useEffect, useCallback } from 'react'; // ADDED: useCallback
import '../styles/ChatBox.css';

function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const [chatError, setChatError] = useState(null); // ADDED: State for chat-specific errors

  // NOTE: This sessionId is hardcoded. In a real application, you might want to generate
  // this dynamically or associate it with the logged-in user.
  const sessionId = "6d6e6c01-a728-4cd9-9ef3-94fe80e52632";

  // ADDITION: Helper function to get auth token from localStorage
  const getAuthToken = useCallback(() => {
    return localStorage.getItem('accessToken');
  }, []);

  // ADDITION: Function to refresh token if necessary (copied from other components)
  const refreshAuthToken = useCallback(async () => {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
      console.warn("No refresh token found. User needs to log in for chat functionality.");
      setChatError("Please log in to use the chat."); // Set a chat-specific error
      // ALTERATION: Redirect to login if no refresh token
      alert("No active session. Please log in.");
      window.location.href = '/login';
      return null;
    }

    try {
      const response = await fetch('https://website3-ho1y.onrender.com/api/users/token/refresh/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: refreshToken }),
      });

      if (!response.ok) {
        console.error("Failed to refresh token:", await response.json());
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        setChatError("Session expired. Please log in again.");
        alert("Session expired. Please log in again.");
        window.location.href = '/login'; // Redirect to login
        return null;
      }

      const data = await response.json();
      localStorage.setItem('accessToken', data.access);
      console.log("Access token refreshed.");
      return data.access;
    } catch (err) {
      console.error("Error refreshing token:", err);
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      setChatError("Error refreshing session. Please log in again.");
      alert("Error refreshing session. Please log in again.");
      window.location.href = '/login'; // Redirect to login
      return null;
    }
  }, []); // Dependencies for useCallback

  // ALTERATION: fetchChatHistory now includes authentication logic
  const fetchChatHistory = useCallback(async (retryCount = 0) => {
    setChatError(null); // Clear previous errors
    let accessToken = getAuthToken();

    if (!accessToken) {
      // If no token, or token expired, try to refresh
      accessToken = await refreshAuthToken();
      if (!accessToken) {
        setChatError("Authentication required to fetch chat history.");
        return; // Stop if no token after refresh
      }
    }

    try {
      const response = await fetch(`https://website3-ho1y.onrender.com/api/chat/chat-history/${sessionId}/`, {
        headers: {
          'Authorization': `Bearer ${accessToken}`, // KEY ADDITION: Include the JWT token
        },
      });

      if (response.status === 401 || response.status === 403) {
        if (retryCount < 1) { // Only retry once
          accessToken = await refreshAuthToken();
          if (accessToken) {
            // Retry request with new token
            return fetchChatHistory(retryCount + 1); // Recursive call for retry
          }
        }
        throw new Error('Authentication required to fetch chat history.');
      } else if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to load chat history');
      } else {
        const data = await response.json();
        setMessages(data.chat_history || []);
      }
    } catch (error) {
      console.error("Error fetching chat history:", error);
      setChatError(error.message); // Set the error message
    }
  }, [sessionId, getAuthToken, refreshAuthToken]); // Dependencies for useCallback

  // ALTERATION: useEffect now triggers fetchChatHistory based on isOpen and its dependencies
  useEffect(() => {
    if (isOpen) {
      fetchChatHistory();
    }
  }, [isOpen, fetchChatHistory]); // fetchChatHistory itself is a dependency now

  // ALTERATION: sendMessage now includes authentication logic
  const sendMessage = async () => {
    const trimmed = input.trim();
    if (!trimmed) return;

    setMessages(prev => [...prev, { sender: "You", text: trimmed }]);
    setInput("");
    setLoading(true);
    setChatError(null); // Clear errors before sending new message

    let accessToken = getAuthToken();

    // If no token, or token expired, try to refresh
    if (!accessToken) {
      accessToken = await refreshAuthToken();
      if (!accessToken) {
        setLoading(false);
        setMessages(prev => [...prev, { sender: "Bot", text: "⚠️ You need to be logged in to send messages." }]);
        return; // Stop if no token after refresh
      }
    }

    try {
      const response = await fetch("https://website3-ho1y.onrender.com/api/chat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          'Authorization': `Bearer ${accessToken}`, // KEY ADDITION: Include the JWT token
        },
        body: JSON.stringify({ message: trimmed, session_id: sessionId })
      });

      if (response.status === 401 || response.status === 403) {
        // If 401/403, try refreshing token ONCE and retry the request
        accessToken = await refreshAuthToken();
        if (accessToken) {
          // Retry the request with the new token
          const retryResponse = await fetch("https://website3-ho1y.onrender.com/api/chat/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              'Authorization': `Bearer ${accessToken}`,
            },
            body: JSON.stringify({ message: trimmed, session_id: sessionId })
          });

          const retryData = await retryResponse.json();
          if (retryResponse.ok) {
            const botReply = retryData.response || "Sorry, I didn't get that.";
            setMessages(prev => [...prev, { sender: "Bot", text: botReply }]);
          } else {
            setMessages(prev => [...prev, { sender: "Bot", text: "⚠️ Error sending message after token refresh: " + (retryData.detail || JSON.stringify(retryData)) }]);
          }
        } else {
          setMessages(prev => [...prev, { sender: "Bot", text: "⚠️ Authentication required to send messages." }]);
        }
      } else if (!response.ok) {
        const errorData = await response.json();
        const errorMessage = errorData.detail || "Failed to get a response from the bot.";
        setMessages(prev => [...prev, { sender: "Bot", text: `⚠️ ${errorMessage}` }]);
      } else {
        const data = await response.json();
        const botReply = data.response || "Sorry, I didn't get that.";
        setMessages(prev => [...prev, { sender: "Bot", text: botReply }]);
      }
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
            {chatError && <p className="chat-error-message">Error: {chatError}</p>} {/* ADDED: Display chat error */}
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