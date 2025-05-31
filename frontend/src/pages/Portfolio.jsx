import React, { useEffect, useState } from 'react';
import TunnelGridBackground from '../components/TunnelGridBackground';
import CompletedProjectsHeader from '../components/CompletedProjectsHeader';
import styles from '../styles/Portfolio.module.css';

function Portfolio() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true); // ✅ Added loading state

  useEffect(() => {
    fetch('https://website3-ho1y.onrender.com/api/portfolio/')
      .then(response => response.json())
      .then(data => {
        setProjects(data);
        setLoading(false); // ✅ Stop loading after data arrives
      })
      .catch(error => {
        console.error('Error fetching projects:', error);
        setLoading(false); // ✅ Also stop loading on error
      });
  }, []);

  return (
    <div className="relative min-h-screen bg-gradient-to-b from-black via-gray-900 to-black">
      <TunnelGridBackground />

      <div className="relative z-10 p-8 max-w-5xl mx-auto text-white">
        <CompletedProjectsHeader />

        {/* ⏳ Show while loading */}
        {loading ? (
          <p className="text-lg animate-pulse">Loading projects...</p>
        ) : projects.length === 0 ? (
          <p className="text-lg text-red-300">No projects found.</p>
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
