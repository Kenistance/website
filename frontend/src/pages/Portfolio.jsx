import React, { useEffect, useState } from 'react';
import TunnelGridBackground from '../components/TunnelGridBackground';
import CompletedProjectPrism from '../components/CompletedProjectPrism';
import styles from '../styles/Portfolio.module.css';

function Portfolio() {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/portfolio/')
      .then(response => response.json())
      .then(data => setProjects(data))
      .catch(error => console.error('Error fetching projects:', error));
  }, []);

  return (
    <div className="relative min-h-screen bg-gradient-to-b from-black via-gray-900 to-black">
      <TunnelGridBackground />

      <div className="relative z-10 p-8 max-w-5xl mx-auto text-white">
        <h1 className="text-4xl font-bold mb-6 drop-shadow-lg">Completed Projects</h1>

        {/* 3D Prism animated text box for completed projects */}
        <CompletedProjectPrism />

        {projects.length === 0 ? (
          <p className="text-lg">No projects found.</p>
        ) : (
          <ul className={styles.projectList}>
            {projects.map(project => (
              <li key={project.id} className={styles.projectItem}>
                <h2 className={styles.projectTitle}>{project.title}</h2>
                <p className={styles.projectDescription}>{project.description}</p>
                {project.image_url && (
                  <img
                    src={project.image_url}
                    alt={project.title}
                    className={styles.projectImage}
                  />
                )}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default Portfolio;
