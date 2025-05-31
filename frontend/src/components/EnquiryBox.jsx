import React, { useState } from 'react';
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

  const handleChange = (e) => {
    const { name, value } = e.target;
    console.log(`Input changed: ${name} = ${value}`);  // Log input changes
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Form submit triggered');
    setSubmitting(true);
    setResponseMessage('');

    try {
      console.log('Sending data:', formData);  // Log data being sent
      const response = await fetch('http://website3-ho1y.onrender.com/api/enquiry/submit/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();
      console.log('Response from server:', data);

      if (response.ok) {
        setResponseMessage(' Enquiry submitted successfully!');
        setFormData({ name: '', email: '', phone: '', message: '' });
      } else {
        setResponseMessage('❌ Error: ' + JSON.stringify(data));
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
