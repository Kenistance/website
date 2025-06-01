import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom'; // Make sure this is from react-router-dom
import '../styles/Requests.css';

function Requests() {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    fetch('https://website3-ho1y.onrender.com/api/requests/requests/')
      .then(res => res.json())
      .then(data => setProjects(data))
      .catch(err => console.error('Failed to fetch project requests:', err));
  }, []);

  return (
    <div className="requests-container">
      <h1 className="page-title">Project Requests</h1>

      <ul className="requests-list">
        {projects.length === 0 ? (
          <p className="no-requests">No requests yet. Be the first to submit yours.</p>
        ) : (
          projects.map(project => (
            <li key={project.id} className="request-card flame">
              <h2>{project.title}</h2>
              <p>Status: <strong>{project.status}</strong></p>
            </li>
          ))
        )}
      </ul>

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
