import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Navbar.css';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-logo">MySite</div>
      <ul className="navbar-links">
        <li><Link to="/" className="nav-link">Home</Link></li>
        <li><Link to="/portfolio" className="nav-link">Portfolio</Link></li>
        <li><Link to="/automation" className="nav-link">Automation</Link></li>
        <li><Link to="/requests" className="nav-link">Requests</Link></li>
      </ul>
    </nav>
  );
}

export default Navbar;
