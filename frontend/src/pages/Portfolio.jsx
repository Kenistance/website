import React, { useEffect, useState } from 'react';

function Portfolio() {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/portfolio/')
      .then(response => response.json())
      .then(data => setProjects(data))
      .catch(error => console.error('Error fetching projects:', error));
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">My Portfolio</h1>
      {projects.length === 0 ? (
        <p>No projects found.</p>
      ) : (
        <ul className="space-y-4">
          {projects.map(project => (
            <li key={project.id} className="border p-4 rounded shadow">
              <h2 className="text-xl font-semibold">{project.title}</h2>
              <p>{project.description}</p>
              {project.image_url && (
                <img src={project.image_url} alt={project.title} className="mt-2 max-w-xs" />
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Portfolio;
