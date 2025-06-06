import React, { useState, useEffect } from 'react';
import { NavLink, useNavigate } from 'react-router-dom'; // Import useNavigate
import '../styles/Navbar.css';

function Navbar() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();

  // Check login status on component mount and when local storage changes
  useEffect(() => {
    const checkLoginStatus = () => {
      const token = localStorage.getItem('accessToken');
      setIsLoggedIn(!!token); // Set to true if token exists, false otherwise
    };

    checkLoginStatus(); // Initial check

    // Optional: Listen for changes in localStorage from other tabs/windows
    window.addEventListener('storage', checkLoginStatus);
    return () => {
      window.removeEventListener('storage', checkLoginStatus);
    };
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    setIsLoggedIn(false); // Update state to reflect logout
    alert('Logged out successfully!');
    navigate('/login'); // Redirect to login page after logout
  };

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
        {/* Conditional authentication links */}
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