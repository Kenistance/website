// src/pages/HomePage.jsx
import React from 'react';
import Navbar from '../components/Navbar';
import EnquiryBox from '../components/EnquiryBox';
import ChatBox from '../components/ChatBox';
import Footer from '../components/Footer';
import '../styles/HomePage.css';

function HomePage() {
  return (
    <>
      {/* Background animation layer */}
      <div className="background-container">
        <div className="rotating-background"></div>
      </div>

      {/* Foreground content */}
      <Navbar />
      <div className="home-container">
        <header className="home-header">
          <h1 className="main-title">Welcome to Code 254</h1>
          <p className="subtitle">Automation • Data Analytics • Custom Projects</p>
        </header>

        <section className="services-section">
          <h2 className="section-title">Services Rendered</h2>
          <div className="services-grid">
            <div className="service-box">Automation solutions to save you time</div>
            <div className="service-box">Data analytics dashboards and insights</div>
            <div className="service-box">AI-assisted tools (chat, data handling)</div>
            <div className="service-box">Custom project builds based on your needs</div>
          </div>
        </section>

        <div className="enquiry-wrapper">
          <div className="enquiry-box">
            <h3>Reach Out </h3>
            <input type="text" placeholder="Your Name" />
            <input type="email" placeholder="Your Email" />
            <textarea rows="4" placeholder="Your Message"></textarea>
            <button>Submit</button>
          </div>
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
