import React, { useState, useCallback } from 'react'; // ADDED: useCallback
import '../styles/EnquiryBox.css';

function EnquiryBox() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    message: ''
  });

  const [submitting, setSubmitting] = useState(false);
  const [responseMessage, setResponseMessage] = useState('');

  // ADDITION: Helper function to get auth token from localStorage
  const getAuthToken = useCallback(() => {
    return localStorage.getItem('accessToken');
  }, []);

  // ADDITION: Function to refresh token if necessary (copied from Portfolio/Requests)
  const refreshAuthToken = useCallback(async () => {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
      console.warn("No refresh token found. User needs to log in to submit enquiry.");
      // ALTERATION: Redirect to login if no refresh token
      alert("No active session. Please log in to submit your enquiry.");
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

  const handleChange = (e) => {
    const { name, value } = e.target;
    console.log(`Input changed: ${name} = ${value}`);
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // ALTERATION: Updated handleSubmit to include authentication logic
  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Form submit triggered');
    setSubmitting(true);
    setResponseMessage('');

    let accessToken = getAuthToken();

    // If no token, or token expired, try to refresh
    if (!accessToken) {
      accessToken = await refreshAuthToken();
      if (!accessToken) {
        setSubmitting(false);
        setResponseMessage('❌ Error: Authentication required to submit enquiry.');
        return; // Stop if no token after refresh
      }
    }

    try {
      console.log('Sending data:', formData);
      const response = await fetch('https://website3-ho1y.onrender.com/api/enquiry/submit/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`, // KEY ADDITION: Include the JWT token
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();
      console.log('Response from server:', data);

      if (response.ok) {
        setResponseMessage('✅ Enquiry submitted successfully!');
        setFormData({ name: '', email: '', phone: '', message: '' });
      } else if (response.status === 401 || response.status === 403) {
        // If 401/403, try refreshing token ONCE and retry the request
        accessToken = await refreshAuthToken();
        if (accessToken) {
          // Retry the request with the new token
          const retryResponse = await fetch('https://website3-ho1y.onrender.com/api/enquiry/submit/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${accessToken}`,
            },
            body: JSON.stringify(formData)
          });

          const retryData = await retryResponse.json();
          if (retryResponse.ok) {
            setResponseMessage('✅ Enquiry submitted successfully!');
            setFormData({ name: '', email: '', phone: '', message: '' });
          } else {
            setResponseMessage('❌ Error submitting enquiry after token refresh: ' + (retryData.detail || JSON.stringify(retryData)));
          }
        } else {
          setResponseMessage('❌ Error: Authentication required to submit enquiry.');
        }
      }
      else {
        setResponseMessage('❌ Error: ' + (data.detail || JSON.stringify(data)));
      }
    } catch (error) {
      console.error('Error submitting enquiry:', error);
      setResponseMessage('❌ Network error. Try again later.');
    }

    setSubmitting(false);
  };

  return (
    <div className="enquiry-container">
      <h2 className="text-xl font-bold mb-2">Make an Enquiry</h2>
      <form onSubmit={handleSubmit} className="enquiry-form">
        <input
          type="text"
          name="name"
          value={formData.name}
          required
          placeholder="Your Name"
          className="w-full border p-2 rounded"
          onChange={handleChange}
        />
        <input
          type="email"
          name="email"
          value={formData.email}
          required
          placeholder="Your Email"
          className="w-full border p-2 rounded"
          onChange={handleChange}
        />
        <input
          type="tel"
          name="phone"
          value={formData.phone}
          required
          placeholder="Your Phone"
          className="w-full border p-2 rounded"
          onChange={handleChange}
        />
        <textarea
          name="message"
          value={formData.message}
          required
          placeholder="Describe your request"
          className="w-full border p-2 rounded"
          onChange={handleChange}
        />
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded w-full"
          disabled={submitting}
        >
          {submitting ? 'Submitting...' : 'Submit'}
        </button>
        {responseMessage && <p className="text-center mt-2">{responseMessage}</p>}
      </form>
    </div>
  );
}

export default EnquiryBox;