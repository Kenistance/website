import React from 'react';
import { NavLink } from 'react-router-dom';
import '../styles/Navbar.css';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-logo">Code 254</div>
      <ul className="navbar-links">
        <li>
          <NavLink to="/" end className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
            Home
          </NavLink>
        </li>
        <li>
          <NavLink to="/portfolio" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
            Portfolio
          </NavLink>
        </li>
        <li>
          <NavLink to="/automation" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
            Automation
          </NavLink>
        </li>
        <li>
          <NavLink to="/requests" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
            Requests
          </NavLink>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
