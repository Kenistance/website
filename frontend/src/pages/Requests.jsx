import React, { useEffect, useState } from 'react';
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
        {projects.map(project => (
          <li key={project.id} className="request-card flame">
            <h2>{project.title}</h2>
            <p>Status: <strong>{project.status}</strong></p>
          </li>
        ))}
      </ul>

      <button className="book-btn">Book Yours by sending an enquiry</button>

      <div className="selling-point">
        <h2>Why Choose Us?</h2>
        <p>
          Fast, reliable, and tailored automation solutions. We turn your ideas into scalable systems with expert precision.
          Whether you are starting a project or scaling up, we are here to make it effortless.
        </p>
      </div>
    </div>
  );
}

export default Requests;
