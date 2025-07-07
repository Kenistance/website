import React, { useEffect, useState } from 'react';
import '../styles/BlogPage.css';

function BlogPage() {
  const [posts, setPosts] = useState([]);
  const [expandedPostId, setExpandedPostId] = useState(null);
  const [error, setError] = useState(null);

  const API_URL = 'https://website3-ho1y.onrender.com/api/blog/posts/';

  useEffect(() => {
    fetch(API_URL, { credentials: 'include' })
      .then(res => {
        if (!res.ok) throw new Error(`Failed to fetch posts: ${res.status}`);
        return res.json();
      })
      .then(data => {
        if (Array.isArray(data)) setPosts(data);
        else setPosts([]);
      })
      .catch(err => {
        console.error("Fetch error:", err.message);
        setError(err.message);
      });
  }, []);

  const toggleReadMore = (id) => {
    setExpandedPostId(prev => (prev === id ? null : id));
  };

  return (
    <div className="blog-container">
      {error && (
        <div className="error-box">Error: {error}</div>
      )}

      {posts.length === 0 && !error && <p>No blog posts found.</p>}

      {posts.map(post => {
        const isExpanded = expandedPostId === post.id;
        const preview = post.content.slice(0, 300);

        return (
          <div key={post.id} className="blog-post">
            <h2>{post.title}</h2>

            {post.image && (
              <img src={post.image} alt={post.title} />
            )}

            <p className="blog-content">
              {isExpanded ? post.content : `${preview}${post.content.length > 300 ? '...' : ''}`}
            </p>

            {post.content.length > 300 && (
              <button onClick={() => toggleReadMore(post.id)} className="read-more-btn">
                {isExpanded ? 'Read Less' : 'Read More'}
              </button>
            )}

            <small>{new Date(post.created_at).toLocaleDateString()}</small>
          </div>
        );
      })}
    </div>
  );
}

export default BlogPage;
