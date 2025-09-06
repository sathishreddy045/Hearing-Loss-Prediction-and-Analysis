import React from 'react';
import apiService from '../../Service/apiService.jsx';
import './Navbar.css';

const Navbar = ({ isLoggedIn, navigate, onLogout }) => {
  
  const handleLogoutClick = async () => {
    try {
      await apiService.logout(); // Call the backend logout endpoint
      onLogout(); // Update the app's state
    } catch (error) {
      console.error("Logout failed", error);
      // Still log out on the frontend even if the backend call fails
      onLogout();
    }
  };

  return (
    <nav className="navbar">
      <a href="#" onClick={() => navigate('home')} className="navbar-logo">
        AudiologyAI
      </a>
      <div className="nav-links">
        {isLoggedIn ? (
          <>
            <a href="#" onClick={() => navigate('home')} className="nav-link">Home</a>
            <a href="#" onClick={() => navigate('features')} className="nav-link">Features</a>
            <a href="#" onClick={() => navigate('prediction')} className="nav-link">Prediction</a>
            <a href="#" onClick={() => navigate('analysis')} className="nav-link">Analysis</a>
            <a href="#" onClick={() => navigate('contact')} className="nav-link">Contact</a>
            <button onClick={handleLogoutClick} className="nav-button">Logout</button>
          </>
        ) : (
          <>
            <a href="#" onClick={() => navigate('home')} className="nav-link">Home</a>
            <button onClick={() => navigate('login')} className="nav-button">Login</button>
            <button onClick={() => navigate('signup')} className="nav-button primary">Sign Up</button>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
