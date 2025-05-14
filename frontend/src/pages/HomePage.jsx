import React from 'react';
import EnquiryBox from '../components/EnquiryBox';
import ChatBox from '../components/ChatBox';

function HomePage() {
  return (
    <div className="p-6">
      <header className="text-center mb-8">
        <h1 className="text-4xl font-bold text-blue-700 mb-2">Welcome to My Portfolio Site</h1>
        <p className="text-gray-600">Automation • Data Analytics • Custom Projects</p>
      </header>

      <section className="max-w-3xl mx-auto mb-10">
        <h2 className="text-2xl font-semibold mb-4">Services I Offer</h2>
        <ul className="list-disc list-inside space-y-2 text-gray-700">
          <li>🔧 Automation solutions to save you time</li>
          <li>📊 Data analytics dashboards and insights</li>
          <li>🧠 AI-assisted tools (chat, data handling)</li>
          <li>📦 Custom project builds based on your needs</li>
        </ul>
      </section>

      {/* Enquiry form */}
      <EnquiryBox />

      {/* Floating chat box */}
      <ChatBox />
    </div>
  );
}

export default HomePage;
