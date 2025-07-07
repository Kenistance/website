import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import { AuthProvider } from './context/AuthContext'; 
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
import PasswordResetRequest from './pages/PasswordResetRequest';
import PasswordResetConfirm from './pages/PasswordResetConfirm';
import BlogPage from './pages/BlogPage';

function App() {
  return (
    <AuthProvider> 
      <Router>
        <ScrollToHash />
        <Navbar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/portfolio" element={<Portfolio />} />
          <Route path="/automation" element={<Automation />} />
          <Route path="/requests" element={<Requests />} />
          <Route path="/company" element={<Company />} />
          <Route path="/terms-policy" element={<TermsPolicy />} />
          <Route path="/payment-success" element={<PaymentSuccess />} />
          <Route path="/payment-cancel" element={<PaymentCancel />} />
          <Route path="/blog" element={<BlogPage />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/request-password-reset" element={<PasswordResetRequest />} />
          <Route path="/reset-password/:uidb64/:token/" element={<PasswordResetConfirm />} />
        </Routes>
        <Footer />
      </Router>
    </AuthProvider>
  );
}

export default App;
