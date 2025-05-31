import React, { useEffect, useState } from 'react';
import EnquiryBox from '../components/EnquiryBox';
import ChatBox from '../components/ChatBox';
import '../styles/HomePage.css';

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

function Cube({ title, details }) {
  const [showFront, setShowFront] = useState(true);

  const handleHover = () => {
    setShowFront(prev => !prev);
  };

  return (
    <div className="cube-wrapper" onMouseEnter={handleHover}>
      <div className={`cube ${showFront ? 'show-front' : 'show-back'}`}>
        <div className="face front">
          <ul>
            {details.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
        <div className="face back">{title}</div>
        <div className="face left">{title}</div>
        <div className="face right">{title}</div>
        <div className="face top">{title}</div>
        <div className="face bottom">{title}</div>
      </div>
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

  useEffect(() => {
    images.forEach((src) => {
      const img = new Image();
      img.src = src;
    });
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      setIsTransitioning(true);
      setTimeout(() => {
        setCurrentImage(nextImage);
        setNextImage((nextImage + 1) % images.length);
        setIsTransitioning(false);
      }, 1000);
    }, 8000);
    return () => clearInterval(interval);
  }, [nextImage]);

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
          <h1 className="main-title">Welcome to Code 254</h1>
          <p className="subtitle">We are the Africa and World's Best</p>
        </header>

        <section className="services-section">
          <h2 className="section-title">We Offer Exceptional Services When It Comes to...</h2>
          <div className="services-grid">
            {services.map((service, i) => (
              <Cube key={i} title={service.title} details={service.details} />
            ))}
          </div>
        </section>

        <div className="enquiry-wrapper">
          <EnquiryBox />
        </div>

        <div className="chatbox-wrapper">
          <ChatBox />
        </div>
      </div>
    </>
  );
}

export default HomePage;
