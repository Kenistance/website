import React, { useEffect, useState } from 'react';
import '../styles/BlogPage.css';

function BlogPage() {
  const [posts, setPosts] = useState([]);
  const [error, setError] = useState(null);

  // 🔁 Live Render endpoint
  const API_URL = 'https://website3-ho1y.onrender.com/api/blog/posts/';

  useEffect(() => {
    console.log("Trying to fetch blog posts...");

    fetch(API_URL, {
      credentials: 'include'  // optional, only needed if auth/session required
    })
      .then(res => {
        console.log("Response status:", res.status);
        if (!res.ok) {
          throw new Error(`Failed to fetch posts: ${res.status}`);
        }
        return res.json();
      })
      .then(data => {
        console.log("Fetched blog posts:", data);
        if (Array.isArray(data)) {
          setPosts(data);
        } else {
          console.warn("Unexpected response structure:", data);
          setPosts([]);
        }
      })
      .catch(err => {
        console.error("Fetch error:", err.message);
        setError(err.message);
        setPosts([]);
      });
  }, []);

  return (
    <div className="p-4 max-w-4xl mx-auto">
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          Error: {error}
        </div>
      )}
  
      {posts.length === 0 && !error && <p>No blog posts found.</p>}
  
      {posts.map(post => (
        <div key={post.id} className="mb-6 p-4 border shadow-sm rounded bg-white">
          <h2 className="text-xl font-semibold mb-2">{post.title}</h2>
  
          {post.image && (
            <img
              src={post.image}
              alt={post.title}
              className="w-full max-h-96 object-cover mb-2 rounded"
            />
          )}
  
          <p className="text-gray-800 whitespace-pre-wrap">{post.content}</p>
  
          <p className="text-sm text-gray-500 mt-2">
            Posted on: {new Date(post.created_at).toLocaleDateString()}
          </p>
        </div>
      ))}
    </div>
  );
  
}

export default BlogPage;
