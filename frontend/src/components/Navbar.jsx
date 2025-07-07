import React, { useContext, useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import '../styles/Navbar.css';
import { AuthContext } from '../context/AuthContext'; // ✅ Import the context

function Navbar() {
  const { isLoggedIn, logout } = useContext(AuthContext); // ✅ Use the context
  const [menuOpen, setMenuOpen] = useState(false);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout(); // ✅ Use the logout function from context
    alert('Logged out successfully!');
    navigate('/login');
  };

  const toggleMenu = () => setMenuOpen(!menuOpen);

  return (
    <nav className="navbar">
      <div className="navbar-header">
        <div className="navbar-logo">Code 254</div>
        <div className="hamburger" onClick={toggleMenu}>
          ☰
        </div>
      </div>
      <ul className={`navbar-links ${menuOpen ? 'open' : ''}`}>
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
          <NavLink to="/blog" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
            Blog
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

        {!isLoggedIn ? (
          <>
            <li>
              <NavLink to="/register" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
                Register
              </NavLink>
            </li>
            <li>
              <NavLink to="/login" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
                Login
              </NavLink>
            </li>
          </>
        ) : (
          <li>
            <button onClick={handleLogout} className="nav-link logout-button">
              Logout
            </button>
          </li>
        )}
      </ul>
    </nav>
  );
}

export default Navbar;
