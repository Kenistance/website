// src/pages/Requests.jsx
import React, { useEffect, useState, useCallback } from 'react';
import { Link } from 'react-router-dom';
import '../styles/Requests.css';

function Requests() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true); 
  const [error, setError] = useState(null);     

  // ADDITION: Helper function to get auth token from localStorage
  const getAuthToken = useCallback(() => {
    return localStorage.getItem('accessToken');
  }, []);

  // ADDITION: Function to refresh token if necessary
  const refreshAuthToken = useCallback(async () => {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
      console.warn("No refresh token found. User needs to log in for requests.");
      // ALTERATION: Redirect to login if no refresh token
      alert("No active session. Please log in.");
      window.location.href = '/login';
      return null;
    }

    try {
      const response = await fetch('https://website3-ho1y.onrender.com/api/users/token/refresh/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: refreshToken }),
      });

      if (!response.ok) {
        console.error("Failed to refresh token:", await response.json());
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        alert("Session expired. Please log in again.");
        window.location.href = '/login'; // Redirect to login
        return null;
      }

      const data = await response.json();
      localStorage.setItem('accessToken', data.access);
      console.log("Access token refreshed.");
      return data.access;
    } catch (err) {
      console.error("Error refreshing token:", err);
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      alert("Error refreshing session. Please log in again.");
      window.location.href = '/login'; // Redirect to login
      return null;
    }
  }, []); // Dependencies for useCallback

  // ALTERATION: Updated useEffect to include authentication logic
  const fetchRequests = useCallback(async () => {
    setLoading(true);
    setError(null);
    let accessToken = getAuthToken();

    if (!accessToken) {
      // If no token, or token expired, try to refresh
      accessToken = await refreshAuthToken();
      if (!accessToken) {
        setLoading(false);
        setError("Please log in to view project requests."); // User must be authenticated
        return;
      }
    }

    try {
      const response = await fetch('https://website3-ho1y.onrender.com/api/requests/requests/', {
        headers: {
          'Authorization': `Bearer ${accessToken}`, // KEY ADDITION: Include the JWT token
        },
      });

      if (response.status === 401 || response.status === 403) {
        // If 401/403, try refreshing token once
        accessToken = await refreshAuthToken();
        if (accessToken) {
          // Retry request with new token
          const retryResponse = await fetch('https://website3-ho1y.onrender.com/api/requests/requests/', {
            headers: {
              'Authorization': `Bearer ${accessToken}`, // KEY ADDITION: Retry with new token
            },
          });
          if (!retryResponse.ok) {
            throw new Error('Failed to load project requests after token refresh.');
          }
          const data = await retryResponse.json();
          setProjects(data);
        } else {
          // Still no valid token after refresh
          throw new Error('Authentication required to view project requests.');
        }
      } else if (!response.ok) {
        const errorData = await response.json(); // Attempt to read error message from response
        throw new Error(errorData.detail || 'Failed to load project requests');
      } else {
        const data = await response.json();
        setProjects(data);
      }
    } catch (err) {
      console.error('Error fetching project requests:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [getAuthToken, refreshAuthToken]); // Dependencies for useCallback

  useEffect(() => {
    fetchRequests();
  }, [fetchRequests]); // Run fetchRequests when the component mounts or fetchRequests changes

  return (
    <div className="requests-container">
      <h1 className="page-title">Project Requests</h1>

      {/* ALTERATION: Conditional rendering for loading, error, and no projects */}
      {loading && <p className="loading-message">Loading project requests...</p>}
      {error && <p className="error-message">Error: {error}</p>}

      {!loading && !error && projects.length === 0 ? (
        <p className="no-requests">No requests yet. Be the first to submit yours.</p>
      ) : (
        <ul className="requests-list">
          {!loading && !error && projects.map(project => (
            <li key={project.id} className="request-card flame">
              <h2>{project.title}</h2>
              <p>Status: <strong>{project.status}</strong></p>
            </li>
          ))}
        </ul>
      )}

      {/* Link to Enquiry Section */}
      <Link to="/#enquiry" className="book-btn">
        Book Yours by Sending an Enquiry <span className="arrow">→ Click Here</span>
      </Link>

      <div className="selling-point">
        <h2>Why Choose Us?</h2>
        <p>
          Fast, reliable, and tailored automation solutions. We turn your ideas into scalable systems with expert precision.
          Whether you're starting a project or scaling up, we are here to make it effortless.
        </p>
      </div>
    </div>
  );
}

export default Requests;