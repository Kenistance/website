import React from 'react';

function Requests() {
  const projects = [
    { id: 1, title: 'Automation for Client A', status: 'In Progress' },
    { id: 2, title: 'Portfolio Site Setup', status: 'Completed' },
    { id: 3, title: 'Data Dashboard', status: 'Pending' },
  ];

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Project Requests</h1>
      <ul className="space-y-4">
        {projects.map(project => (
          <li key={project.id} className="border p-4 rounded shadow">
            <h2 className="text-xl font-semibold">{project.title}</h2>
            <p>Status: <strong>{project.status}</strong></p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Requests;
