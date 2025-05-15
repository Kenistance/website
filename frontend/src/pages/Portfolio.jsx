import React, { useEffect, useState } from 'react';
import styles from '../styles/Portfolio.module.css'; // use module

function Portfolio() {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/portfolio/')
      .then(response => response.json())
      .then(data => setProjects(data))
      .catch(error => console.error('Error fetching projects:', error));
  }, []);

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>My Portfolio</h1>
      {projects.length === 0 ? (
        <p className={styles.message}>No projects found.</p>
      ) : (
        <ul className={styles.projectList}>
          {projects.map(project => (
            <li key={project.id} className={styles.projectItem}>
              <h2 className={styles.projectTitle}>{project.title}</h2>
              <p>{project.description}</p>
              {project.image_url && (
                <img src={project.image_url} alt={project.title} className={styles.projectImage} />
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Portfolio;
