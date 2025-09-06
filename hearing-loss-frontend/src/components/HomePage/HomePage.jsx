import React from 'react';
import './HomePage.css'; // normal CSS import

const HomePage = ({ navigate }) => {
  return (
    <section className="hero-section">
      <div className="hero-content">
        <h1 className="hero-title">Predictive Insights into Hearing Health</h1>
        <p className="hero-subtitle">
          Leveraging advanced AI to analyze audiological data and provide
          early detection and classification of hearing loss.
        </p>
        <button onClick={() => navigate('prediction')} className="hero-button">
          Check Now
        </button>
      </div>
    </section>
  );
};

export default HomePage;
