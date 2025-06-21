import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [messages, setMessages] = useState([
    { sender: 'Jokester Bot', text: '😂 Welcome! I am Jokester Bot, your over-the-top, witty, and complicated answer machine. Ask me anything—math, facts, or just for a laugh!' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const API_URL = 'http://localhost:5000/api/chat';

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    const userMsg = { sender: 'You', text: input };
    setMessages(msgs => [...msgs, userMsg]);
    setLoading(true);
    setInput('');
    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      });
      const data = await res.json();
      setMessages(msgs => [...msgs, { sender: 'Jokester Bot', text: data.reply }]);
    } catch (err) {
      setMessages(msgs => [...msgs, { sender: 'Jokester Bot', text: '⚠️ Sorry, I could not reach the server.' }]);
    }
    setLoading(false);
  };

  return (
    <div style={{ minHeight: '100vh', background: '#181a1b' }}>
      <div className="container py-5" style={{ maxWidth: 600 }}>
        <div className="card shadow bg-dark text-light border-light">
          <div className="card-header bg-secondary text-warning">
            <h3>😂 Jokester Bot</h3>
            <div style={{ fontSize: '0.95em' }}>
              <span>Ask me anything—math, facts, or just for a laugh!<br />
              I’ll answer in the most complicated, witty, and funny way possible (but always correct!).</span>
            </div>
          </div>
          <div className="card-body" style={{ height: 400, overflowY: 'auto', background: '#23272b' }}>
            {messages.map((msg, idx) => (
              <div key={idx} className={`mb-2 ${msg.sender === 'You' ? 'text-end' : 'text-start'}`}>
                <span className={`badge ${msg.sender === 'You' ? 'bg-info text-dark' : 'bg-warning text-dark'}`}>{msg.sender}</span>
                <div style={{ whiteSpace: 'pre-line' }}>{msg.text}</div>
              </div>
            ))}
            {loading && <div className="text-start"><span className="badge bg-warning text-dark">Jokester Bot</span> <span>Typing...</span></div>}
          </div>
          <form className="card-footer d-flex bg-dark border-top border-light" onSubmit={sendMessage}>
            <input
              className="form-control me-2 bg-secondary text-light border-0"
              type="text"
              placeholder="Ask me anything..."
              value={input}
              onChange={e => setInput(e.target.value)}
              disabled={loading}
              autoFocus
            />
            <button className="btn btn-warning" type="submit" disabled={loading || !input.trim()}>
              Send
            </button>
          </form>
        </div>
        <div className="text-center mt-3" style={{ color: '#fff' }}>
          <small>
            <b>How to use:</b> Just type your question or ask for a joke!<br />
            Jokester Bot will always answer, but expect a little humor and a lot of wit.<br />
            (Type 'fact' for a fun fact!)
          </small>
        </div>
      </div>
    </div>
  );
}

export default App;
