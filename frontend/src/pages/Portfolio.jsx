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

  // Helper function to get auth token
  const getAuthToken = useCallback(() => {
    return localStorage.getItem('accessToken');
  }, []);

  // Function to refresh token if necessary
  const refreshAuthToken = async () => {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
      console.warn("No refresh token found. User needs to log in.");
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
  };

  const fetchProjects = useCallback(async () => {
    setLoading(true);
    setError(null);
    let accessToken = getAuthToken();

    if (!accessToken) {
      // If no token, or token expired, try to refresh
      accessToken = await refreshAuthToken();
      if (!accessToken) {
        setLoading(false);
        // User is not logged in or session expired, Portfolio might show public content
        // or a message to log in. For now, it will show error as IsAuthenticated is default.
        setError("Please log in to view projects.");
        return;
      }
    }

    try {
      const response = await fetch('https://website3-ho1y.onrender.com/api/portfolio/', {
        headers: {
          'Authorization': `Bearer ${accessToken}`, // Include the JWT token
        },
      });

      if (response.status === 401 || response.status === 403) {
        // If 401/403, try refreshing token once
        accessToken = await refreshAuthToken();
        if (accessToken) {
          // Retry request with new token
          const retryResponse = await fetch('https://website3-ho1y.onrender.com/api/portfolio/', {
            headers: {
              'Authorization': `Bearer ${accessToken}`,
            },
          });
          if (!retryResponse.ok) {
            throw new Error('Failed to load projects after refresh.');
          }
          const data = await retryResponse.json();
          setProjects(data);
        } else {
          // Still no valid token after refresh
          throw new Error('Authentication required to view projects.');
        }
      } else if (!response.ok) {
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
  }, [getAuthToken, refreshAuthToken]); // Include dependencies

  useEffect(() => {
    fetchProjects();
  }, [fetchProjects]); // Run fetchProjects when the component mounts or fetchProjects changes

  const handleStripePayment = async (project) => {
    setPaymentLoading(`stripe-${project.id}`);
    const authToken = getAuthToken();
    if (!authToken) {
      alert("Please log in to make payments.");
      // You might want to redirect to login page here
      return;
    }

    try {
      const response = await fetch('https://website3-ho1y.onrender.com/api/payments/stripe-checkout/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authToken}`, // Important: send token
        },
        body: JSON.stringify({ project_id: project.id }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Stripe checkout failed');
      }

      const data = await response.json();
      window.location.href = data.checkout_url; // Redirect to Stripe checkout page
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
      // You might want to redirect to login page here
      return;
    }

    // You might need to prompt for phone number here if not stored in user profile
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
          'Authorization': `Bearer ${authToken}`, // Important: send token
        },
        body: JSON.stringify({ project_id: project.id, phone_number: phoneNumber }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.errorMessage || 'M-Pesa payment failed');
      }

      const data = await response.json();
      alert(data.message || 'M-Pesa payment initiated. Please check your phone.');
      // You might want to periodically check status or listen for webhooks here
    } catch (err) {
      alert(`M-Pesa payment error: ${err.message}`);
      console.error('M-Pesa payment error:', err);
    } finally {
      setPaymentLoading(null);
    }
  };

  const handleFreeDownload = (project) => {
    alert(`Downloading ${project.title} for free! (Not implemented yet)`);
    // Implement actual free download logic here (e.g., redirect to file)
  };

  return (
    <div className={styles.portfolioPage}>
      <TunnelGridBackground />
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
                <h3 className={styles.projectTitle}>{project.title}</h3>
                <p className={styles.projectDescription}>{project.description}</p>
                <div className={styles.paymentSection}>
                  {project.price > 0 ? (
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