import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Navbar from './components/Navbar';
import Footer from './components/Footer';
import ScrollToHash from './components/ScrollToHash'; 

import HomePage from './pages/HomePage';
import Portfolio from './pages/Portfolio';
import Automation from './pages/Automation';
import Requests from './pages/Requests';
import Company from './pages/Company';
import TermsPolicy from './pages/TermsPolicy';



function App() {
  return (
    <Router>
      <ScrollToHash />
      <Navbar />   {/* Always visible */}
      
      {/* Page content */}
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/portfolio" element={<Portfolio />} />
        <Route path="/automation" element={<Automation />} />
        <Route path="/requests" element={<Requests />} />
        <Route path="/company" element={<Company />} />
        <Route path="/terms-policy" element={<TermsPolicy />} />
      </Routes>

      <Footer />   {/* Now this shows on all pages */}
    </Router>
  );
}

export default App;
