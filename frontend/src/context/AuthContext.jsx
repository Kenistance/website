import React, { createContext, useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode'; // ✅ Correct import

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // ✅ Validate token
  const isTokenValid = (token) => {
    try {
      const decoded = jwtDecode(token);
      const now = Math.floor(Date.now() / 1000); // current time in seconds
      return decoded.exp > now;
    } catch (err) {
      return false;
    }
  };

  useEffect(() => {
    const accessToken = localStorage.getItem('accessToken');
    if (accessToken && isTokenValid(accessToken)) {
      setIsLoggedIn(true);
    } else {
      logout(); // Log out if token is missing or invalid
    }

    const checkLoginStatus = () => {
      const token = localStorage.getItem('accessToken');
      if (token && isTokenValid(token)) {
        setIsLoggedIn(true);
      } else {
        logout();
      }
    };

    window.addEventListener('storage', checkLoginStatus);
    return () => window.removeEventListener('storage', checkLoginStatus);
  }, []);

  const login = (access, refresh) => {
    localStorage.setItem('accessToken', access);
    localStorage.setItem('refreshToken', refresh);
    setIsLoggedIn(true);
  };

  const logout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    setIsLoggedIn(false);
  };

  return (
    <AuthContext.Provider value={{ isLoggedIn, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
