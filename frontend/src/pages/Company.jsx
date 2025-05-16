import React from 'react';
import '../styles/Company.css';

const Company = () => {
  return (
    <div className="company-page">
      <section id="about">
        <h2>About</h2>
        <p>
          At Code 254, we stand at the forefront of technological innovation, empowering businesses,
          governments, and communities across Africa and beyond to harness the full potential of data
          and intelligent systems. Our mission is to deliver cutting-edge solutions that drive
          efficiency, foster growth, and create sustainable impact.
        </p>

        <p>Our expertise centers around four key pillars, each delivering tangible value across diverse industries:</p>

        <h3>Data Analytics</h3>
        <p>
          We specialize in transforming complex data into clear, actionable insights that fuel smarter
          decision-making. Our advanced data collection, visualization, and predictive modeling enable
          clients to anticipate market trends, optimize operations, and unlock hidden opportunities.
        </p>
        <ul>
          <li><strong>Agriculture:</strong> Improving crop yields through precision analytics that predict weather patterns, soil health, and pest outbreaks using sensor data and satellite imagery.</li>
          <li><strong>Healthcare:</strong> Assisting hospitals in patient outcome prediction, resource optimization, and disease outbreak tracking for better care and cost management.</li>
          <li><strong>Banking & Finance:</strong> Enhancing fraud detection, customer segmentation, and risk management by analyzing transactions and behaviors.</li>
          <li><strong>Manufacturing:</strong> Enabling predictive maintenance, quality control monitoring, and supply chain optimization to reduce downtime and improve productivity.</li>
        </ul>

        <h3>Automation</h3>
        <p>
          Our bespoke automation solutions streamline repetitive workflows, minimize errors, and free up valuable
          human resources for higher-value tasks.
        </p>
        <ul>
          <li><strong>Agriculture:</strong> Automated irrigation systems and supply chain tracking to reduce waste and increase efficiency.</li>
          <li><strong>Healthcare:</strong> Automation of patient record management, appointment scheduling, and billing to enhance operational efficiency.</li>
          <li><strong>Banking & Finance:</strong> Automated compliance checks, loan processing workflows, and chatbots improving turnaround and customer service.</li>
          <li><strong>Manufacturing:</strong> Robotic process automation (RPA) and assembly line integration improving throughput and product consistency.</li>
        </ul>

        <h3>Artificial Intelligence</h3>
        <p>
          Leveraging AI, we build intelligent systems that revolutionize business operations and customer interaction,
          unlocking new value streams with machine learning, natural language processing, and more.
        </p>
        <ul>
          <li><strong>Agriculture:</strong> AI-driven drone monitoring for early crop disease detection and optimized pesticide application.</li>
          <li><strong>Healthcare:</strong> AI-assisted medical image analysis, personalized treatments, and virtual health assistants.</li>
          <li><strong>Banking & Finance:</strong> AI-powered credit scoring, fraud detection, and conversational AI platforms enhancing decisions and engagement.</li>
          <li><strong>Manufacturing:</strong> AI optimizing production scheduling, defect detection, and supply forecasting.</li>
        </ul>

        <h3>Custom Projects</h3>
        <p>
          We recognize every client’s needs are unique. Our collaborative approach ensures tailored solutions aligned to your specific challenges and goals.
        </p>
        <ul>
          <li>Mobile apps for remote agricultural data collection linked to real-time analytics dashboards.</li>
          <li>Integrated hospital management systems with embedded AI diagnostics.</li>
          <li>Secure, compliant fintech platforms tailored to emerging market regulations.</li>
          <li>IoT-enabled smart factory solutions synchronizing equipment and logistics for lean manufacturing.</li>
        </ul>

        <p>
          At Code 254, we blend global best practices with deep local insights to deliver advanced, compliant,
          and ethical technology solutions. Partner with us to transform your data into your greatest asset,
          automate for efficiency, and leverage AI to stay ahead in an evolving technological landscape.
        </p>
      </section>

      <section id="careers">
        <h2>Careers</h2>
        <p>
          Join a vibrant and dynamic team where innovation thrives. At Code 254, we foster a culture
          of continuous learning, collaboration, and impact. Our career opportunities are designed
          to help you grow professionally and personally.
        </p>

        <h3>Developer</h3>
        <p>
          As a developer, you will work on full-stack applications that solve real-world problems.
          You will collaborate across teams to design scalable, secure software, and implement new
          features that drive business value. Experience with JavaScript frameworks, cloud services,
          and CI/CD pipelines is a plus.
        </p>

        <h3>Data Engineer</h3>
        <p>
          Our data engineers build and maintain robust data pipelines that handle large datasets efficiently.
          You will design ETL processes, optimize databases, and support analytics platforms that enable
          powerful insights. Familiarity with SQL, Python, and big data technologies is essential, and knowledge of other programming languages such as JavaScript, Java, Bash, PowerShell, and Ruby commonly used in automation is highly valued
        </p>

        <h3>Automation Engineer</h3>
        <p>
          Automation engineers at Code 254 create and manage solutions that automate workflows across
          sectors. You will develop scripts, integrate APIs, and implement robotic process automation
          to improve operational efficiency. Experience with scripting languages, cloud automation,
          and DevOps tools is beneficial.
        </p>

        <p>
          We offer competitive salaries, ongoing training, flexible work arrangements, and the chance
          to make a real difference in industries ranging from agriculture and healthcare to banking
          and manufacturing.
        </p>
      </section>

      <section id="sitemap">
        <h2>Sitemap</h2>
        <ul className="sitemap-list">
          <li><a href="/">Home</a></li>
          <li><a href="/portfolio">Portfolio</a></li>
          <li><a href="/automation">Automation</a></li>
          <li><a href="/requests">Requests</a></li>
          <li><a href="/company#about">About</a></li>
          <li><a href="/company#careers">Careers</a></li>
          <li><a href="/company#affiliate">Affiliate Program</a></li>
          <li><a href="/terms-policy#terms">Terms of Service</a></li>
          <li><a href="/terms-policy#privacy">Privacy Policy</a></li>
          <li><a href="/terms-policy#cookie">Cookie Policy</a></li>
          <li><a href="/terms-policy#preferences">Cookie Preferences</a></li>
        </ul>
      </section>

      <section id="affiliate">
        <h2>Become an Affiliate</h2>
        <p>
          Are you passionate about technology and eager to connect businesses with the tools they need
          to succeed? Join our Affiliate Program and become a vital part of the Code 254 growth story.
        </p>

        <p>
          As an affiliate, you act as the bridge between potential clients and our cutting-edge solutions.
          Whether you have a network in agriculture, healthcare, banking, manufacturing, or any other
          industry, your connections can open doors to transformative partnerships.
        </p>

        <p>
          We offer an attractive 20% commission on every successful deal you help close, alongside
          comprehensive support to empower you with marketing materials, technical insights, and
          dedicated affiliate management.
        </p>

        <p>
          Whether you are a consultant, industry expert, or simply someone with a passion for technology,
          our affiliate program offers an excellent opportunity to monetize your network and grow your
          income by promoting innovative solutions that make a difference.
        </p>

        <p>
          Become a partner with Code 254 and help shape the future of technology adoption across Africa
          and beyond.
        </p>
      </section>
    </div>
  );
};

export default Company;
