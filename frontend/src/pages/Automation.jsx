import React from 'react';
import styles from '../styles/Automation.module.css';

function Automation() {
  const services = [
    {
      title: "Excel/Google Sheets Automation",
      details: [
        "Auto reports generation",
        "Data cleanup & formatting",
        "Dashboards & charts"
      ]
    },
    {
      title: "Data Scraping & Cleanup",
      details: [
        "Extract data from websites",
        "Clean & structure messy datasets",
        "Automate data collection"
      ]
    },
    {
      title: "Email Automation",
      details: [
        "Send batch emails",
        "Auto replies & alerts",
        "Extract email content"
      ]
    },
    {
      title: "Custom Python Scripts",
      details: [
        "Automate repetitive tasks",
        "Integrate APIs & tools",
        "Build tailored workflows"
      ]
    },
    {
      title: "Web Scraping & API Integration",
      details: [
        "Track prices, trends, updates",
        "Pull structured data via APIs",
        "Build data pipelines"
      ]
    },
    {
      title: "Document Automation",
      details: [
        "Generate PDFs, reports, invoices",
        "Extract info from Word or PDF",
        "Fill forms automatically"
      ]
    },
    {
      title: "Chatbot & Messaging Automation",
      details: [
        "Telegram, Discord, Slack bots",
        "Auto chat replies",
        "Customer support integrations"
      ]
    },
    {
      title: "Task Scheduling & Monitoring",
      details: [
        "Daily or weekly automated tasks",
        "Error alerts and status logging",
        "Background script management"
      ]
    },
    {
      title: "GUI/Desktop Automation",
      details: [
        "Mouse & keyboard simulation",
        "UI testing",
        "Automated form filling"
      ]
    }
  ];

  return (
    <div className={styles.container}>
      <div className={styles.introBox}>
        <h1 className={styles.title}>Automation Services</h1>
        <p className={styles.subtext}>
          We offer a variety of Python-based automation services to save you time, reduce manual effort, and improve productivity.
        </p>
      </div>
      <div className={styles.grid}>
        {services.map((service, index) => (
          <div key={index} className={styles.cube}>
            <div className={styles.front}>
              <h2 className={styles.cardTitle}>{service.title}</h2>
              <ul className={styles.list}>
                {service.details.map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            </div>
            <div className={styles.back}>
              <h3>Learn More</h3>
              <p>Contact us for more info about {service.title.toLowerCase()}.</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Automation;
