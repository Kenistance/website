import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'; // No longer need Link directly in App.js

import Navbar from './components/Navbar';
import Footer from './components/Footer';
import ScrollToHash from './components/ScrollToHash';

import HomePage from './pages/HomePage';
import Portfolio from './pages/Portfolio';
import Automation from './pages/Automation';
import Requests from './pages/Requests';
import Company from './pages/Company';
import TermsPolicy from './pages/TermsPolicy';
import PaymentSuccess from './pages/PaymentSuccess';
import PaymentCancel from './pages/PaymentCancel';
import Register from './pages/Register';
import Login from './pages/Login';

function App() {
  return (
    <Router>
      <ScrollToHash />
      <Navbar /> {/* Your Navbar now handles all navigation and auth links */}

      {/* The conditional authentication links and logout button were here, now removed */}

      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/portfolio" element={<Portfolio />} />
        <Route path="/automation" element={<Automation />} />
        <Route path="/requests" element={<Requests />} />
        <Route path="/company" element={<Company />} />
        <Route path="/terms-policy" element={<TermsPolicy />} />
        <Route path="/payment-success" element={<PaymentSuccess />} />
        <Route path="/payment-cancel" element={<PaymentCancel />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
      </Routes>

      <Footer />
    </Router>
  );
}

export default App;