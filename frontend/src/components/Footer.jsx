import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Footer.css';

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-top">
        {/* Company Section */}
        <div className="footer-section">
          <h3>Company</h3>
          <ul>
            <li><Link to="/company#about">About</Link></li>
            <li><Link to="/company#careers">Careers</Link></li>
            <li><Link to="/company#sitemap">Sitemap</Link></li>
            <li><Link to="/company#affiliate">Become an Affiliate</Link></li>
          </ul>
        </div>

        {/* Terms & Policy Section */}
        <div className="footer-section">
          <h3>Terms & Policy</h3>
          <ul>
            <li><Link to="/terms-policy#terms">Terms of Service</Link></li>
            <li><Link to="/terms-policy#privacy">Privacy Policy</Link></li>
            <li><Link to="/terms-policy#cookie">Cookie Policy</Link></li>
            <li><Link to="/terms-policy#preferences">Cookie Preferences</Link></li>
          </ul>
        </div>

        {/* Contact Us Section */}
        <div className="footer-section">
          <h3>Contact Us</h3>
          <ul className="contact-info">
            <li><i className="fas fa-envelope"></i> <a href="mailto:kennedysmithaz@gmail.com">kennedysmithaz@gmail.com</a></li>
            <li><i className="fas fa-phone"></i> <a href="tel:+254706776303">+254 706 776 303</a></li>
            <li><i className="fas fa-map-marker-alt"></i> <Link to="/contact">Nairobi, Kenya</Link></li>
          </ul>
        </div>

        {/* Social Media Section */}
        <div className="footer-section">
          <h3>Connect</h3>
          <div className="footer-socials">
            <a href="https://www.facebook.com/" target="_blank" rel="noopener noreferrer"><i className="fab fa-facebook-f"></i></a>
            <a href="https://web.whatsapp.com/" target="_blank" rel="noopener noreferrer"><i className="fab fa-whatsapp"></i></a>
            <a href="https://twitter.com/" target="_blank" rel="noopener noreferrer"><i className="fab fa-twitter"></i></a>
            <a href="https://www.snapchat.com/" target="_blank" rel="noopener noreferrer"><i className="fab fa-snapchat-ghost"></i></a>
            <a href="https://www.tiktok.com/" target="_blank" rel="noopener noreferrer"><i className="fab fa-tiktok"></i></a>
          </div>
        </div>
      </div>

      {/* Bottom copyright */}
      <div className="footer-bottom">
        © {new Date().getFullYear()} Code 254. All rights reserved.
      </div>
    </footer>
  );
}

export default Footer;
