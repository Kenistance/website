import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import HomePage from './pages/HomePage';
import Portfolio from './pages/Portfolio';
import Automation from './pages/Automation';
import Requests from './pages/Requests';

function App() {
  return (
    <Router>
      <nav className="bg-gray-100 p-4">
        <Link to="/" className="mr-4">Home</Link>
        <Link to="/portfolio" className="mr-4">Portfolio</Link>
        <Link to="/automation" className="mr-4">Automation</Link>
        <Link to="/requests" className="mr-4">Requests</Link>
      </nav>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/portfolio" element={<Portfolio />} />
        <Route path="/automation" element={<Automation />} />
        <Route path="/requests" element={<Requests />} />
      </Routes>
    </Router>
  );
}

export default App;
