// src/App.jsx
import React, { useState } from 'react';
import Navbar from './components/Navbar/Navbar.jsx';
import HomePage from './components/HomePage/HomePage.jsx';
import { LoginPage } from './components/Auth/LoginPage/LoginPage.jsx'; // Corrected path
import { SignupPage } from './components/Auth/SignupPage/SignupPage.jsx'; // Corrected path
import PredictionPage from './components/PredictionPage/PredictionPage.jsx';
import AnalysisPage from './components/AnalysisPage/AnalysisPage.jsx';
import Footer from './components/Footer/Footer.jsx';

const App = () => {
  const [page, setPage] = useState('home');
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const navigate = (targetPage) => {
    setPage(targetPage);
  };

  const handleLogin = () => {
    setIsLoggedIn(true);
    setPage('home');
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setPage('home');
  };

  const renderPage = () => {
    switch (page) {
      case 'home':
        return <HomePage navigate={navigate} />;
      case 'login':
        return <LoginPage onLogin={handleLogin} navigate={navigate} />;
      case 'signup':
        return <SignupPage onSignup={handleLogin} navigate={navigate} />;
      case 'prediction':
        return <PredictionPage />;
      case 'analysis':
        return <AnalysisPage />;
      default:
        return <HomePage navigate={navigate} />;
    }
  };

  return (
    <>
      <Navbar isLoggedIn={isLoggedIn} navigate={navigate} onLogout={handleLogout} />
      <main>
        {renderPage()}
      </main>
      <Footer />
    </>
  );
}

export default App;
