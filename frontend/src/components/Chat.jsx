import React, { useState } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import './Chat.css';

function Chat() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    { role: 'system', content: '你好，我是周易AI助手，有什么关于周易的问题可以问我。' }
  ]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      // Assuming backend is proxying to GLM
      // In a real app, we should maintain context or send previous messages if the API supports it
      // Here we just send the last message for simplicity or adjust backend to handle history
      const res = await axios.post('/api/chat', { message: input });
      
      // Parse GLM response structure
      // GLM API returns a JSON with 'choices'
      let aiContent = "无法获取回答";
      if (res.data && res.data.choices && res.data.choices.length > 0) {
          aiContent = res.data.choices[0].message.content;
      } else if (res.data.error) {
          aiContent = "Error: " + res.data.error;
      }

      setMessages(prev => [...prev, { role: 'assistant', content: aiContent }]);
    } catch (err) {
      console.error(err);
      setMessages(prev => [...prev, { role: 'assistant', content: '网络错误或API调用失败' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-window">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <div className="message-content">
              {msg.role === 'assistant' ? (
                                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                                ) : (
                                  msg.content
                                )}
            </div>
          </div>
        ))}
        {loading && <div className="message assistant"><div className="message-content">思考中...</div></div>}
      </div>
      <form onSubmit={handleSubmit} className="chat-input-area">
        <input 
          type="text" 
          value={input} 
          onChange={(e) => setInput(e.target.value)} 
          placeholder="输入你的问题..." 
        />
        <button type="submit" disabled={loading}>发送</button>
      </form>
    </div>
  );
}

export default Chat;
