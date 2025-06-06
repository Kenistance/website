// src/pages/PasswordResetRequest.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from '../styles/Auth.module.css'; 

function PasswordResetRequest() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleRequestReset = async (e) => {
    e.preventDefault();
    setMessage(null);
    setError(null);
    setLoading(true);

    try {
      const response = await fetch('https://website3-ho1y.onrender.com/api/users/request-password-reset/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.email || errorData.detail || 'Failed to send reset email.');
      }

      const data = await response.json();
      setMessage(data.detail || 'Password reset email sent. Please check your inbox.');
      setEmail(''); // Clear the email field

    } catch (err) {
      setError(err.message);
      console.error('Password reset request error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.authContainer}>
      <div className={styles.authBox}>
        <h2>Request Password Reset</h2>
        <form onSubmit={handleRequestReset}>
          {message && <p className={styles.success}>{message}</p>}
          {error && <p className={styles.error}>{error}</p>}
          <div className={styles.formGroup}>
            <label htmlFor="email">Email:</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <button type="submit" disabled={loading} className={styles.authButton}>
            {loading ? 'Sending...' : 'Send Reset Email'}
          </button>
        </form>
        <p className={styles.toggleLink}>
          Remembered your password? <span onClick={() => navigate('/login')}>Login here</span>
        </p>
      </div>
    </div>
  );
}

export default PasswordResetRequest;