import React from 'react';
import '../styles/Footer.css';

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-top">
        <div className="footer-section">
          <h3>Company</h3>
          <ul>
            <li><a href="#">About</a></li>
            <li><a href="#">Careers</a></li>
            <li><a href="#">Sitemap</a></li>
            <li><a href="#">Become an Affiliate</a></li>
          </ul>
        </div>

        <div className="footer-section">
          <h3>Terms & Policy</h3>
          <ul>
            <li><a href="#">Terms of Service</a></li>
            <li><a href="#">Privacy policy</a></li>
            <li><a href="#">Cookie policy</a></li>
            <li><a href="#">Cookie preferences</a></li>
          </ul>
        </div>

        <div className="footer-section">
          <h3>Connect</h3>
          <div className="footer-socials">
            <a href="#"><i className="fab fa-facebook-f"></i></a>
            <a href="#"><i className="fab fa-whatsapp"></i></a>
            <a href="#"><i className="fab fa-twitter"></i></a>
            <a href="#"><i className="fab fa-snapchat-ghost"></i></a>
            <a href="#"><i className="fab fa-tiktok"></i></a>
          </div>
        </div>
      </div>

      <div className="footer-bottom">
        © {new Date().getFullYear()} Your Company. All rights reserved.
      </div>
    </footer>
  );
}

export default Footer;
