import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import './HexagramList.css';

function HexagramList() {
  const [hexagrams, setHexagrams] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [showChat, setShowChat] = useState(false);
  const [showSearchModal, setShowSearchModal] = useState(false);
  const [searchResults, setSearchResults] = useState([]);
  const [searchLoading, setSearchLoading] = useState(false);
  const [chatInput, setChatInput] = useState('');
  const [chatMessages, setChatMessages] = useState([
    { role: 'system', content: '我是周易AI助手，请问有什么可以帮您？' }
  ]);
  const [chatLoading, setChatLoading] = useState(false);
  
  const navigate = useNavigate();

  useEffect(() => {
    axios.get('/api/hexagrams')
      .then(res => setHexagrams(res.data))
      .catch(err => console.error(err));
  }, []);

  // Helper to highlight text
  const getHighlightedText = (text, highlight) => {
    // 1. Remove Markdown/HTML noise for display
    let cleanText = text
        .replace(/!\[.*?\]\(.*?\)/g, '') // Remove images
        .replace(/<.*?>/g, '') // Remove HTML tags
        .replace(/(\*\*|__)(.*?)\1/g, '$2') // Remove bold
        .replace(/(\*|_)(.*?)\1/g, '$2') // Remove italic
        .replace(/^#+\s+/gm, '') // Remove headers
        .replace(/>\s+/gm, '') // Remove blockquotes
        .replace(/\n+/g, ' '); // Collapse newlines
    
    // 2. Find the index of the search query
    const lowerText = cleanText.toLowerCase();
    const lowerHighlight = highlight.toLowerCase();
    const index = lowerText.indexOf(lowerHighlight);
    
    if (index === -1) return cleanText.substring(0, 100) + '...';
    
    // 3. Extract a window of text around the match
    const start = Math.max(0, index - 30);
    const end = Math.min(cleanText.length, index + highlight.length + 50);
    const snippet = (start > 0 ? '...' : '') + cleanText.substring(start, end) + (end < cleanText.length ? '...' : '');

    // 4. Highlight the match
    const parts = snippet.split(new RegExp(`(${highlight})`, 'gi'));
    return (
      <span>
        {parts.map((part, i) => 
          part.toLowerCase() === lowerHighlight ? 
            <mark key={i} style={{backgroundColor: '#ffeb3b', padding: '0 2px', borderRadius: '2px'}}>{part}</mark> : part
        )}
      </span>
    );
  };

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      setShowSearchModal(true);
      setSearchLoading(true);
      axios.get(`/api/hexagrams/search?q=${searchQuery}`)
        .then(res => {
          setSearchResults(res.data);
          setSearchLoading(false);
        })
        .catch(err => {
          console.error(err);
          setSearchLoading(false);
        });
    }
  };

  const handleStartReading = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      handleSearch(e);
    } else {
        const grid = document.querySelector('.hexagram-grid');
        if (grid) grid.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleAIButtonClick = (e) => {
    // Stop form submission if inside a form, though type="button" should prevent it.
    // Explicitly prevent default just in case.
    if (e) e.preventDefault();
    
    if (searchQuery.trim()) {
        setChatInput(searchQuery);
        setSearchQuery('');
        setShowChat(true);
    } else {
        setShowChat(prev => !prev);
    }
  };

  const handleChatSubmit = async (e) => {
    e.preventDefault();
    if (!chatInput.trim()) return;

    const userMsg = { role: 'user', content: chatInput };
    setChatMessages(prev => [...prev, userMsg]);
    setChatInput('');
    setChatLoading(true);

    try {
      const res = await axios.post('/api/chat', { message: chatInput });
      let aiContent = "无法获取回答";
      if (res.data && res.data.choices && res.data.choices.length > 0) {
          aiContent = res.data.choices[0].message.content;
      } else if (res.data.error) {
          // Fix: Handle object error properly
          if (typeof res.data.error === 'object') {
             aiContent = "Error: " + JSON.stringify(res.data.error);
          } else {
             aiContent = "Error: " + res.data.error;
          }
      }
      setChatMessages(prev => [...prev, { role: 'assistant', content: aiContent }]);
    } catch (err) {
      console.error(err);
      setChatMessages(prev => [...prev, { role: 'assistant', content: '网络错误或API调用失败' }]);
    } finally {
      setChatLoading(false);
    }
  };

  return (
    <div className="home-container">
      {/* Hero Section */}
      <section className="hero-section">
        <h1 className="hero-title">刚健中正 顺天应人</h1>
        <p className="hero-subtitle">为往圣继绝学 为万世开太平</p>
        
        {/* Search & AI Entry */}
        <div className="hero-interaction">
          <form onSubmit={handleStartReading} className="hero-search-form">
            <input 
              type="text" 
              placeholder="搜索周易内容..." 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button type="submit" className="read-btn">开始阅读</button>
            <button type="button" className="ai-btn" onClick={handleAIButtonClick}>
              AI 智能问答
            </button>
          </form>

          {/* AI Chat Popup - Moved inside hero-interaction for correct positioning */}
          {showChat && (
            <div className="hero-chat-popup">
              <div className="chat-header">
                <span>周易 AI 助手</span>
                <button onClick={() => setShowChat(false)}>×</button>
              </div>
              <div className="chat-body">
                {chatMessages.map((msg, idx) => (
                  <div key={idx} className={`chat-message ${msg.role}`}>
                  {msg.role === 'assistant' ? (
                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                  ) : (
                    msg.content
                  )}
                </div>
                ))}
                {chatLoading && <div className="chat-message assistant">思考中...</div>}
              </div>
              <form onSubmit={handleChatSubmit} className="chat-footer">
                <input 
                  type="text" 
                  value={chatInput} 
                  onChange={(e) => setChatInput(e.target.value)}
                  placeholder="询问周易相关问题..." 
                />
                <button type="submit" disabled={chatLoading}>发送</button>
              </form>
            </div>
          )}
        </div>
        {showSearchModal && (
          <div className="modal-overlay" onClick={() => setShowSearchModal(false)}>
            <div className="modal-content" onClick={e => e.stopPropagation()}>
              <div className="modal-header">
                 <h2>搜索结果</h2>
                 <button className="close-btn" onClick={() => setShowSearchModal(false)}>×</button>
              </div>
              <div className="modal-body">
                {searchLoading ? <div className="loading">搜索中...</div> : (
                   searchResults.length > 0 ? (
                      <ul className="search-result-list">
                        {searchResults.map(res => (
                           <li key={res.id}>
                             <Link to={`/read/${res.id}`}>
                               <h3>第{res.id}卦 {res.name}</h3>
                               <p>{getHighlightedText(res.fullText, searchQuery)}</p>
                             </Link>
                           </li>
                        ))}
                      </ul>
                   ) : <div className="no-result">未找到相关内容</div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* AI Chat Popup */}
        {/* Removed duplicate popup rendering from here */}
      </section>

      {/* Hexagram Grid */}
      <div className="hexagram-grid">
        {hexagrams.map(hex => (
          <Link key={hex.id} to={`/read/${hex.id}`} className="hexagram-card">
            <img src={hex.imageUrl.startsWith('/') ? hex.imageUrl : `/${hex.imageUrl}`} alt={hex.name} className="hexagram-image" />
            <div className="hexagram-info">
              <span className="hexagram-number">{hex.id}</span>
              <span className="hexagram-name">{hex.name}</span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}

export default HexagramList;
