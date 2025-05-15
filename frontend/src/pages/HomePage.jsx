import React, { useEffect, useState } from 'react';
import EnquiryBox from '../components/EnquiryBox';
import ChatBox from '../components/ChatBox';
import Footer from '../components/Footer';
import '../styles/HomePage.css';

function HomePage() {
  // List your background images here (adjust paths as needed)
  const images = [
    '/assets/planet1.jpg',
    '/assets/galaxy.jpg',
    '/assets/starscape.jpg'
  ];

  // State to track which image is shown
  const [currentImage, setCurrentImage] = useState(0);

  // Change image every 10 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentImage((prev) => (prev + 1) % images.length);
    }, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <>
      {/* Background animation layer with rotating images */}
      <div className="background-container">
        <div
          className="rotating-background"
          style={{ backgroundImage: `url(${images[currentImage]})` }}
        ></div>
      </div>

      {/* Foreground content - unchanged */}
      <div className="home-container">
        <header className="home-header">
          <h1 className="main-title">Welcome to Code 254</h1>
          <p className="subtitle">We are the Africa and Worlds Best</p>
        </header>

        <section className="services-section">
          <h2 className="section-title">Services Rendered</h2>
          <div className="services-grid">
            {/* Cube 1 - Automation */}
            <div className="cube-wrapper">
              <div className="cube">
                <div className="face front">
                  <ul>
                    <li>Automate repetitive tasks</li>
                    <li>Optimize workflows</li>
                    <li>Improve productivity</li>
                  </ul>
                </div>
                <div className="face back">Automation</div>
                <div className="face left">Automation</div>
                <div className="face right">Automation</div>
                <div className="face top">Automation</div>
                <div className="face bottom">Automation</div>
              </div>
            </div>

            {/* Cube 2 - Data Analytics */}
            <div className="cube-wrapper">
              <div className="cube">
                <div className="face front">
                  <ul>
                    <li>Data collection & visualization</li>
                    <li>Actionable insights for decisions</li>
                    <li>Predictive analytics for trends</li>
                  </ul>
                </div>
                <div className="face back">Data Analytics</div>
                <div className="face left">Data Analytics</div>
                <div className="face right">Data Analytics</div>
                <div className="face top">Data Analytics</div>
                <div className="face bottom">Data Analytics</div>
              </div>
            </div>

            {/* Cube 3 - AI Tools */}
            <div className="cube-wrapper">
              <div className="cube">
                <div className="face front">
                  <ul>
                    <li>AI-powered solutions</li>
                    <li>Automation with machine learning</li>
                    <li>Data-driven decision-making</li>
                  </ul>
                </div>
                <div className="face back">AI Tools</div>
                <div className="face left">AI Tools</div>
                <div className="face right">AI Tools</div>
                <div className="face top">AI Tools</div>
                <div className="face bottom">AI Tools</div>
              </div>
            </div>

            {/* Cube 4 - Custom Projects */}
            <div className="cube-wrapper">
              <div className="cube">
                <div className="face front">
                  <ul>
                    <li>Tailored project development</li>
                    <li>End-to-end solutions</li>
                    <li>Innovative problem-solving</li>
                  </ul>
                </div>
                <div className="face back">Custom Projects</div>
                <div className="face left">Custom Projects</div>
                <div className="face right">Custom Projects</div>
                <div className="face top">Custom Projects</div>
                <div className="face bottom">Custom Projects</div>
              </div>
            </div>
          </div>
        </section>

        <div className="enquiry-wrapper">
          <EnquiryBox />
        </div>

        <div className="chatbox-wrapper">
          <ChatBox />
        </div>
      </div>
      <Footer />
    </>
  );
}

export default HomePage;
