import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import HexagramList from './components/HexagramList';
import Reading from './components/Reading';
import Search from './components/Search';
import Chat from './components/Chat';
import './App.css';

function App() {
  return (
    <Router basename="/book/ZhouYi">
      <div className="app-container">
        <nav className="navbar">
          <Link to="/" className="brand">周易 Digital</Link>
          <div className="nav-links">
            <Link to="/">首页</Link>
            <Link to="/search">搜索</Link>
            <Link to="/chat">AI问答</Link>
          </div>
        </nav>
        <div className="content">
          <Routes>
            <Route path="/" element={<HexagramList />} />
            <Route path="/read/:id" element={<Reading />} />
            <Route path="/search" element={<Search />} />
            <Route path="/chat" element={<Chat />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
