import React, { useState } from 'react';

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
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setResponseMessage('');

    try {
      const response = await fetch('http://127.0.0.1:8000/api/enquiry/submit/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (response.ok) {
        setResponseMessage('✅ Enquiry submitted successfully!');
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
    <div className="mt-8 border p-4 rounded shadow max-w-md mx-auto">
      <h2 className="text-xl font-bold mb-2">Make an Enquiry</h2>
      <form onSubmit={handleSubmit} className="space-y-2">
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
