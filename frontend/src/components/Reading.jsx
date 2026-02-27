import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import rehypeRaw from 'rehype-raw';
import './Reading.css';

function Reading() {
  const { id } = useParams();
  const [hexagram, setHexagram] = useState(null);
  const [allHexagrams, setAllHexagrams] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch all hexagrams for the sidebar
    axios.get('/api/hexagrams')
      .then(res => setAllHexagrams(res.data))
      .catch(err => console.error(err));
  }, []);

  useEffect(() => {
    setLoading(true);
    axios.get(`/api/hexagrams/${id}`)
      .then(res => {
        const data = res.data;
        // Fix image paths in fullText if they are relative
        if (data.fullText) {
             // Only replace 'images/' with '/images/' if it doesn't start with '/'
             data.fullText = data.fullText.replace(/\]\(images\//g, '](/images/');
        }
        setHexagram(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, [id]);

  if (loading) return <div className="loading">加载中...</div>;
  if (!hexagram) return <div className="error">未找到该卦</div>;

  return (
    <div className="reading-container">
      <aside className="sidebar-left">
        <h3>六十四卦目录</h3>
        <ul>
          {allHexagrams.map(h => (
            <li key={h.id} className={h.id === parseInt(id) ? 'active' : ''}>
              <Link to={`/read/${h.id}`}>{h.id}. {h.name}</Link>
            </li>
          ))}
        </ul>
      </aside>
      
      <main className="content-main">
        <div className="hexagram-header">
           <h1>第{hexagram.id}卦 {hexagram.name}</h1>
           <img src={hexagram.imageUrl.startsWith('/') ? hexagram.imageUrl : `/${hexagram.imageUrl}`} alt={hexagram.name} className="hexagram-symbol-large" />
        </div>
        <div className="markdown-content">
          <ReactMarkdown rehypePlugins={[rehypeRaw]}>{hexagram.fullText}</ReactMarkdown>
        </div>
      </main>
      
      <aside className="sidebar-right">
        <h3>本卦结构</h3>
        <div className="yao-list">
          {/* Display Yaos from top (Shang) to bottom (Chu) visually */}
          {/* If hexagram.yaos is not populated, generate from binaryCode */}
          {hexagram.yaos && hexagram.yaos.length > 0 ? (
              [...hexagram.yaos].reverse().map((yao, index) => (
                 <div key={yao.id} className={`yao-item ${yao.yang ? 'yang' : 'yin'}`}>
                   <div className="yao-line">
                      {yao.yang ? <div className="solid-line"></div> : <div className="broken-line"><span></span><span></span></div>}
                   </div>
                   <span className="yao-name">{yao.name}</span>
                 </div>
              ))
           ) : (
             /* Fallback: Parse binaryCode (e.g. "111111") */
             hexagram.binaryCode && hexagram.binaryCode.split('').reverse().map((bit, index) => {
                 // binaryCode in data: "010001" (Bottom -> Top)
                 // But we are mapping reverse() of split array?
                 // Wait.
                 // binaryCode: "101101" (Bottom -> Top, i.e. Chu -> Shang)
                 // split: ['1', '0', '1', '1', '0', '1'] (0=Chu, 5=Shang)
                 // reverse: ['1', '0', '1', '1', '0', '1'] (0=Shang, 5=Chu)
                 
                 const isYang = bit === '1';
                 
                 // Calculate original position index (0=Chu, 5=Shang)
                 // If we reversed the array, then current index 0 is Shang (pos 5), index 5 is Chu (pos 0).
                 const originalPos = 5 - index; 
                 
                 const positionChar = ['初', '二', '三', '四', '五', '上'][originalPos];
                 const yinYangChar = isYang ? '九' : '六';
                 
                 let fullName = '';
                 if (originalPos === 0) fullName = `初${yinYangChar}`; // e.g. 初九
                 else if (originalPos === 5) fullName = `上${yinYangChar}`; // e.g. 上六
                 else fullName = `${yinYangChar}${positionChar}`; // e.g. 六二, 九三
                 
                 return (
                    <div key={index} className={`yao-item ${isYang ? 'yang' : 'yin'}`}>
                      <div className="yao-line">
                         {isYang ? <div className="solid-line"></div> : <div className="broken-line"><span></span><span></span></div>}
                      </div>
                      <span className="yao-name">{fullName}</span>
                    </div>
                 );
             })
          )}
        </div>
        <div className="hexagram-info-box">
            <p><strong>编码:</strong> {hexagram.binaryCode}</p>
        </div>
      </aside>
    </div>
  );
}

export default Reading;
