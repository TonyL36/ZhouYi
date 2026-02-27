import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './Search.css';

function Search() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [searched, setSearched] = useState(false);

  const handleSearch = (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    axios.get(`/api/hexagrams/search?q=${query}`)
      .then(res => {
        setResults(res.data);
        setSearched(true);
      })
      .catch(err => console.error(err));
  };

  return (
    <div className="search-page">
      <div className="search-header">
        <h1>周易全文搜索</h1>
        <form onSubmit={handleSearch}>
          <input 
            type="text" 
            value={query} 
            onChange={e => setQuery(e.target.value)} 
            placeholder="输入卦名或卦辞..." 
          />
          <button type="submit">搜索</button>
        </form>
      </div>

      <div className="search-results">
        {searched && results.length === 0 && <p>未找到相关内容。</p>}
        {results.map(hex => (
          <div key={hex.id} className="search-item">
            <Link to={`/read/${hex.id}`}>
              <h3>{hex.name} (第{hex.id}卦)</h3>
            </Link>
            <p className="preview">
              {hex.fullText.substring(0, 100)}...
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Search;
