// src/pages/HomePage.jsx
import React, { useEffect, useState, useCallback } from 'react';
import EnquiryBox from '../components/EnquiryBox';
import ChatBox from '../components/ChatBox';
import '../styles/HomePage.css'; // Make sure this CSS file is updated as well

const services = [
  {
    title: "Automation",
    details: ["Automate repetitive tasks", "Optimize workflows", "Improve productivity"]
  },
  {
    title: "Data Analytics",
    details: ["Data collection & visualization", "Actionable insights for decisions", "Predictive analytics for trends"]
  },
  {
    title: "AI Tools",
    details: ["AI-powered solutions", "Automation with machine learning", "Data-driven decision-making"]
  },
  {
    title: "Custom Projects",
    details: ["Tailored project development", "End-to-end solutions", "Innovative problem-solving"]
  }
];

// ServiceCard component - no 'icon' prop
function ServiceCard({ title, details }) {
  return (
    <div className="service-card">
      <h3 className="service-card-title">{title}</h3>
      <ul className="service-card-details">
        {details.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

function HomePage() {
  const images = [
    '/assets/planet1.jpg',
    '/assets/galaxy.jpg',
    '/assets/starscape.jpg'
  ];

  const [currentImage, setCurrentImage] = useState(0);
  const [nextImage, setNextImage] = useState(1);
  const [isTransitioning, setIsTransitioning] = useState(false);

  // Preload images
  useEffect(() => {
    images.forEach((src) => {
      const img = new Image();
      img.src = src;
    });
  }, [images]);

  // Background image rotation
  useEffect(() => {
    const interval = setInterval(() => {
      setIsTransitioning(true);
      setTimeout(() => {
        setCurrentImage(nextImage);
        setNextImage((prevNextImage) => (prevNextImage + 1) % images.length);
        setIsTransitioning(false);
      }, 1000);
    }, 8000);
    return () => clearInterval(interval);
  }, [nextImage, images.length]);

  // Function to scroll to the enquiry section
  const scrollToEnquiry = useCallback(() => {
    document.getElementById('enquiry').scrollIntoView({ behavior: 'smooth' });
  }, []);

  return (
    <>
      <div className="background-container">
        <div
          className={`rotating-background ${isTransitioning ? 'fade-out' : 'fade-in'}`}
          style={{ backgroundImage: `url(${images[currentImage]})` }}
        />
        <div
          className={`rotating-background next-background ${isTransitioning ? 'fade-in' : 'fade-out'}`}
          style={{ backgroundImage: `url(${images[nextImage]})` }}
        />
      </div>

      <div className="home-container">
        <header className="home-header">
          <h1 className="main-title">Code254: Smart Digital Solutions</h1>
          <p className="subtitle">We build custom websites, AI tools, Automation tools with python and data systems to solve real problems — for Africa and beyond.</p>
          <button className="cta-button" onClick={scrollToEnquiry}>
            Get a Free Consultation
          </button>
        </header>

        <section className="services-section">
          <h2 className="section-title">We Offer Exceptional Services In...</h2>
          <div className="services-grid">
            {services.map((service, i) => (
              <ServiceCard key={i} title={service.title} details={service.details} />
            ))}
          </div>
        </section>

        <section id="enquiry" className="enquiry-wrapper">
          <h2 className="section-title">Let's Talk About Your Project</h2>
          <p className="subtitle">Tell us what you're looking for — we will respond within 24 hours.</p>
          <EnquiryBox />
        </section>

        <div className="chatbox-wrapper">
          <ChatBox />
        </div>
      </div>
    </>
  );
}

export default HomePage;