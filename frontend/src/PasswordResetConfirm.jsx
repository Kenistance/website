// src/pages/PasswordResetConfirm.jsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import styles from '../styles/Auth.module.css'; 

function PasswordResetConfirm() {
  const { uidb64, token } = useParams(); // Get UID and token from URL parameters
  const navigate = useNavigate();
  const [password, setPassword] = useState('');
  const [password2, setPassword2] = useState('');
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isLinkValid, setIsLinkValid] = useState(true); // State to check link validity

  // Optionally, you might want to perform an initial check on uidb64/token
  // with the backend if you have an endpoint for it, but the SetNewPasswordSerializer
  // handles this validation on submission.

  const handlePasswordReset = async (e) => {
    e.preventDefault();
    setMessage(null);
    setError(null);
    setLoading(true);

    try {
      const response = await fetch('https://website3-ho1y.onrender.com/api/users/reset-password-confirm/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          uidb64,
          token,
          password,
          password2,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        // Backend errors for password reset confirm typically come from serializer validation
        throw new Error(errorData.password || errorData.password2 || errorData.non_field_errors || errorData.detail || 'Password reset failed.');
      }

      const data = await response.json();
      setMessage(data.detail || 'Your password has been reset successfully!');
      setTimeout(() => {
        navigate('/login'); // Redirect to login after successful reset
      }, 3000); // Redirect after 3 seconds

    } catch (err) {
      setError(err.message);
      console.error('Password reset confirm error:', err);
      // If the link was invalid/expired, set isLinkValid to false
      if (err.message.includes("Invalid or expired reset link")) {
        setIsLinkValid(false);
      }
    } finally {
      setLoading(false);
    }
  };

  // You might want to do a basic check on mount if uidb64 or token are missing
  useEffect(() => {
    if (!uidb64 || !token) {
      setError("Invalid password reset link. Missing UID or token.");
      setIsLinkValid(false);
    }
  }, [uidb64, token]);


  if (!isLinkValid) {
    return (
      <div className={styles.authContainer}>
        <div className={styles.authBox}>
          <h2>Invalid Link</h2>
          <p className={styles.error}>The password reset link is invalid or has expired.</p>
          <p className={styles.toggleLink}>
            <span onClick={() => navigate('/request-password-reset')}>Request a new reset link</span>
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.authContainer}>
      <div className={styles.authBox}>
        <h2>Set New Password</h2>
        <form onSubmit={handlePasswordReset}>
          {message && <p className={styles.success}>{message}</p>}
          {error && <p className={styles.error}>{error}</p>}
          <div className={styles.formGroup}>
            <label htmlFor="password">New Password:</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className={styles.formGroup}>
            <label htmlFor="password2">Confirm New Password:</label>
            <input
              type="password"
              id="password2"
              value={password2}
              onChange={(e) => setPassword2(e.target.value)}
              required
            />
          </div>
          <button type="submit" disabled={loading} className={styles.authButton}>
            {loading ? 'Resetting...' : 'Reset Password'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default PasswordResetConfirm;