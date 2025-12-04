import React, { useState } from 'react'

export default function App() {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  async function sendMessage() {
    if (!input.trim()) return
    const userMsg = { role: 'user', text: input }
    setMessages((m) => [...m, userMsg])
    setInput('')
    setLoading(true)

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg.text })
      })
      const data = await res.json()
      if (data.reply) {
        setMessages((m) => [...m, { role: 'bot', text: data.reply }])
      } else if (data.error) {
        setMessages((m) => [...m, { role: 'bot', text: 'Error: ' + data.error }])
      }
    } catch (e) {
      setMessages((m) => [...m, { role: 'bot', text: 'Network error' }])
    } finally {
      setLoading(false)
    }
  }

  function onKey(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="container">
      <h1>Chat</h1>
      <div className="chat-window">
        {messages.map((m, i) => (
          <div key={i} className={`msg ${m.role}`}>
            <div className="role">{m.role === 'user' ? 'You' : 'Bot'}</div>
            <div className="text">{m.text}</div>
          </div>
        ))}
        {loading && <div className="msg bot">Bot is typing...</div>}
      </div>

      <div className="composer">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={onKey}
          placeholder="Type your message and press Enter"
        />
        <button onClick={sendMessage} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  )
}
