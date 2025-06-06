// src/pages/Portfolio.jsx
import React, { useEffect, useState, useCallback } from 'react';
import CompletedProjectsHeader from '../components/CompletedProjectsHeader';
import styles from '../styles/Portfolio.module.css';

function Portfolio() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [paymentLoading, setPaymentLoading] = useState(null); // Track which payment is processing

  // Helper function to get auth token from localStorage
  const getAuthToken = useCallback(() => {
    return localStorage.getItem('accessToken');
  }, []);

  // Function to refresh token if necessary
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
  }, []);

  // Main function to fetch projects with authentication logic
  const fetchProjects = useCallback(async () => {
    setLoading(true);
    setError(null);
    let accessToken = getAuthToken();

    // The ProjectListView is now public, so no token is strictly required for *fetching* the list.
    // However, if other parts of your app or future features require authentication for some project details,
    // this logic remains useful. For now, we allow fetching without a token for the public list.
    let headers = {};
    if (accessToken) {
      headers['Authorization'] = `Bearer ${accessToken}`;
    }

    try {
      const response = await fetch('https://website3-ho1y.onrender.com/api/portfolio/', { headers });

      if (!response.ok) {
        // If the backend returns an error even for public access (e.g., 500), handle it.
        throw new Error('Failed to load projects');
      } else {
        const data = await response.json();
        setProjects(data);
      }
    } catch (err) {
      console.error('Error fetching projects:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [getAuthToken]); // Removed refreshAuthToken from dependencies if not strictly needed for initial fetch

  useEffect(() => {
    fetchProjects();
  }, [fetchProjects]);

  const handleStripePayment = async (project) => {
    setPaymentLoading(`stripe-${project.id}`);
    const authToken = getAuthToken();
    if (!authToken) {
      alert("Please log in to make payments.");
      window.location.href = '/login';
      return;
    }

    try {
      const response = await fetch('https://website3-ho1y.onrender.com/api/payments/stripe-checkout/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authToken}`,
        },
        body: JSON.stringify({ project_id: project.id }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Stripe checkout failed');
      }

      const data = await response.json();
      window.location.href = data.checkout_url;
    } catch (err) {
      alert(`Payment error: ${err.message}`);
      console.error('Stripe payment error:', err);
    } finally {
      setPaymentLoading(null);
    }
  };

  const handleMpesaPayment = async (project) => {
    setPaymentLoading(`mpesa-${project.id}`);
    const authToken = getAuthToken();
    if (!authToken) {
      alert("Please log in to make payments.");
      window.location.href = '/login';
      return;
    }

    const phoneNumber = prompt("Please enter your M-Pesa phone number (e.g., 2547XXXXXXXX):");
    if (!phoneNumber) {
      setPaymentLoading(null);
      return; // User cancelled
    }

    try {
      const response = await fetch('https://website3-ho1y.onrender.com/api/payments/mpesa-payment/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authToken}`,
        },
        body: JSON.stringify({ project_id: project.id, phone_number: phoneNumber }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.errorMessage || 'M-Pesa payment failed');
      }

      const data = await response.json();
      alert(data.message || 'M-Pesa payment initiated. Please check your phone.');
    } catch (err) {
      alert(`M-Pesa payment error: ${err.message}`);
      console.error('M-Pesa payment error:', err);
    } finally {
      setPaymentLoading(null);
    }
  };

  // Modified handleFreeDownload to use project.download_url
  const handleFreeDownload = (project) => {
    if (project.download_url) {
      window.open(project.download_url, '_blank'); // Open download URL in a new tab
    } else {
      alert(`No direct download link available for ${project.title}.`);
    }
  };

  // New function to handle visiting website projects
  const handleVisitWebsite = (project) => {
    if (project.website_url) {
      window.open(project.website_url, '_blank'); // Open website URL in a new tab
    } else {
      alert(`No website URL available for ${project.title}.`);
    }
  };


  return (
    <div className={styles.portfolioPage}>
      {/* REMOVED: <TunnelGridBackground /> */}
      <div className={styles.content}>
        <CompletedProjectsHeader />
        {loading && <p>Loading projects...</p>}
        {error && <p className={styles.error}>Error: {error}</p>}
        {!loading && !error && projects.length === 0 && (
          <p>No projects available. Please log in or check your backend.</p>
        )}
        {!loading && !error && projects.length > 0 && (
          <ul className={styles.projectList}>
            {projects.map((project) => (
              <li key={project.id} className={styles.projectItem}>
                {/* Display image if available */}
                {project.image_url && (
                  <img src={project.image_url} alt={project.title} className={styles.projectImage} />
                )}
                <h3 className={styles.projectTitle}>{project.title}</h3>
                <p className={styles.projectDescription}>{project.description}</p>
                <div className={styles.paymentSection}>
                  {project.project_type && project.project_type.toLowerCase() === 'website' && project.website_url ? (
                    // Render "Visit Website" button for website projects
                    <button
                      onClick={() => handleVisitWebsite(project)}
                      className={`${styles.paymentButton} ${styles.websiteButton}`}
                    >
                      Visit Website
                    </button>
                  ) : project.project_type && project.project_type.toLowerCase() === 'program' ? (
                    // Render payment/download options for program projects
                    project.price > 0 ? (
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
                      <button
                        onClick={() => handleFreeDownload(project)}
                        className={`${styles.paymentButton} ${styles.downloadButton}`}
                      >
                        Download Free
                      </button>
                    )
                  ) : (
                    // Fallback if project_type is not defined, not 'website', or not 'program'
                    <p>Link coming soon.</p>
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