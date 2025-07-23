import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [chatLog, setChatLog] = useState([]);
  const [theme, setTheme] = useState('dark');
  const [isTyping, setIsTyping] = useState(false);
  const chatContainerRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [chatLog]);

  const sendMessage = async () => {
    const trimmedMessage = message.trim();
    if (!trimmedMessage) return;

    // Add user message to chat log
    setChatLog(prev => [...prev, { sender: 'You', text: trimmedMessage }]);
    setMessage('');
    setIsTyping(true);

    try {
      const res = await axios.post('http://localhost:5000/chat', { 
        message: trimmedMessage 
      });
      
      // Add bot response to chat log
      setChatLog(prev => [...prev, { 
        sender: "Azan's Agent 🤖", 
        text: res.data.response 
      }]);
    } catch (err) {
      setChatLog(prev => [...prev, { 
        sender: "Azan's Agent", 
        text: '⚠️ Error contacting the backend. Please try again.' 
      }]);
    } finally {
      setIsTyping(false);
    }
  };

  const toggleTheme = () => {
    setTheme(prev => (prev === 'dark' ? 'pink' : 'dark'));
  };
  
  useEffect(() => {
    document.body.className = theme;
  }, [theme]);
  
  return (
    <div className="App">
      <div className="chat-frame">
        <header className="header">
          <h1 className={`bot-title ${theme}`}>Azan's Agent</h1>
          <button 
            className="theme-toggle"
            onClick={toggleTheme}
            aria-label="Toggle theme"
          >
            {theme === 'dark' ? '🌸 Pink Mode' : '🌑 Dark Mode'}
          </button>
        </header>
  
        <div className="chat-container" ref={chatContainerRef}>
          {chatLog.map((entry, index) => (
            <div
              key={index}
              className={`message-row ${entry.sender === 'You' ? 'align-right' : 'align-left'}`}
            >
              <div className={`message ${entry.sender === 'You' ? 'user' : 'bot'}`}>
                {entry.sender === 'You' ? '' : <strong>Azan's Agent:</strong>}
                <div className="message-text">{entry.text}</div>
              </div>
            </div>
          ))}
          
          {isTyping && (
            <div className="message-row align-left">
              <div className="message bot typing-indicator">
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
              </div>
            </div>
          )}
        </div>

        <div className="input-box">
          <input
            type="text"
            value={message}
            placeholder="Type a message..."
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            aria-label="Type your message"
          />
          <button 
            onClick={sendMessage}
            disabled={!message.trim() || isTyping}
          >
            {isTyping ? 'Sending...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;