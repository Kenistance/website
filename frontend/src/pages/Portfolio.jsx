// src/pages/Portfolio.jsx
import React, { useEffect, useState, useCallback } from 'react';
import TunnelGridBackground from '../components/TunnelGridBackground';
import CompletedProjectsHeader from '../components/CompletedProjectsHeader';
import styles from '../styles/Portfolio.module.css';

function Portfolio() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [paymentLoading, setPaymentLoading] = useState(null); // Track which payment is processing

  // Get auth token from localStorage
  const getAuthToken = useCallback(() => {
    return localStorage.getItem('accessToken');
  }, []);

  // Refresh token if expired or missing
  const refreshAuthToken = useCallback(async () => {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
      console.warn("No refresh token found. User needs to log in.");
      alert("No active session. Please log in.");
      window.location.href = '/login';
      return null;
    }

    try {
      const response = await fetch('https://website3-ho1y.onrender.com/api/users/token/refresh/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: refreshToken }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error("Failed to refresh token. Server response:", errorText);
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        alert("Session expired or invalid. Please log in again.");
        window.location.href = '/login';
        return null;
      }

      const data = await response.json();
      localStorage.setItem('accessToken', data.access);
      // Update refresh token if new one is returned (sliding tokens)
      if (data.refresh) {
        localStorage.setItem('refreshToken', data.refresh);
      }
      console.log("Token refreshed successfully.");
      return data.access;
    } catch (err) {
      console.error("Error refreshing token:", err);
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      alert("An error occurred during session refresh. Please log in again.");
      window.location.href = '/login';
      return null;
    }
  }, []);

  // Fetch portfolio projects with token management
  const fetchProjects = useCallback(async () => {
    setLoading(true);
    setError(null);

    let token = getAuthToken();

    if (!token) {
      token = await refreshAuthToken();
      if (!token) {
        setLoading(false);
        return;
      }
    }

    try {
      let response = await fetch('https://website3-ho1y.onrender.com/api/portfolio/', {
        headers: { Authorization: `Bearer ${token}` },
      });

      // If token expired, try to refresh once more and retry request
      if (response.status === 401) {
        console.warn("Access token expired. Attempting to refresh...");
        token = await refreshAuthToken();
        if (token) {
          response = await fetch('https://website3-ho1y.onrender.com/api/portfolio/', {
            headers: { Authorization: `Bearer ${token}` },
          });
        } else {
          // redirect handled in refreshAuthToken
          return;
        }
      }

      if (!response.ok) {
        const errorText = await response.text();
        console.error("Error fetching portfolio data:", errorText);
        setError(`Failed to load portfolio data. Server response: ${response.status} ${response.statusText}. Check console for details.`);
        return;
      }

      const data = await response.json();
      setProjects(data);
    } catch (err) {
      console.error("Network or parsing error fetching portfolio:", err);
      setError(`Failed to connect to the server or parse data: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }, [getAuthToken, refreshAuthToken]);

  useEffect(() => {
    fetchProjects();
  }, [fetchProjects]);

  // Payment handlers - these should ideally also handle loading state and token refresh if calling APIs
  const handleStripePayment = (project) => {
    alert(`Stripe payment for ${project.title} - $${project.price}`);
    console.log("Stripe payment initiated for project:", project);
  };

  const handleMpesaPayment = (project) => {
    alert(`M-Pesa payment for ${project.title} - $${project.price}`);
    console.log("M-Pesa payment initiated for project:", project);
  };

  const handleFreeDownload = (project) => {
    alert(`Downloading ${project.title} for free.`);
    console.log("Free download initiated for project:", project);
  };

  return (
    <div className={styles.portfolioContainer}>
      <TunnelGridBackground />
      <CompletedProjectsHeader />
      <div className={styles.projectsContent}>
        {loading && <p className={styles.loadingMessage}>Loading projects...</p>}
        {error && <p className={styles.errorMessage}>Error: {error}</p>}
        {!loading && !error && projects.length === 0 && (
          <p className={styles.noProjects}>No projects to display yet.</p>
        )}
        {!loading && !error && projects.length > 0 && (
          <ul className={styles.projectsGrid}>
            {projects.map((project) => (
              <li key={project.id} className={styles.projectCard}>
                <h3 className={styles.projectTitle}>{project.title}</h3>
                <p className={styles.projectDescription}>{project.description}</p>
                {project.image_url && (
                  <img
                    src={project.image_url}
                    alt={project.title}
                    className={styles.projectImage}
                  />
                )}
                <div className={styles.actions}>
                  {project.is_paid_project ? (
                    project.download_link ? (
                      <>
                        <button
                          onClick={() => handleStripePayment(project)}
                          disabled={paymentLoading === `stripe-${project.id}`}
                          className={`${styles.paymentButton} ${styles.stripeButton} ${
                            paymentLoading === `stripe-${project.id}` ? 'opacity-50 cursor-not-allowed' : ''
                          }`}
                        >
                          {paymentLoading === `stripe-${project.id}` ? 'Processing...' : 'Pay with Card'}
                          <span className={styles.priceText}>${project.price}</span>
                        </button>
                        <button
                          onClick={() => handleMpesaPayment(project)}
                          disabled={paymentLoading === `mpesa-${project.id}`}
                          className={`${styles.paymentButton} ${styles.mpesaButton} ${
                            paymentLoading === `mpesa-${project.id}` ? 'opacity-50 cursor-not-allowed' : ''
                          }`}
                        >
                          {paymentLoading === `mpesa-${project.id}` ? 'Processing...' : 'Pay with M-Pesa'}
                          <span className={styles.priceText}>${project.price}</span>
                        </button>
                      </>
                    ) : (
                      <p>Link coming soon.</p>
                    )
                  ) : (
                    <button
                      onClick={() => handleFreeDownload(project)}
                      className={`${styles.paymentButton} ${styles.downloadButton}`}
                    >
                      Download Free
                    </button>
                  )}
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default Portfolio;
