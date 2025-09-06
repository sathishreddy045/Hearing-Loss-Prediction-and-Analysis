import React, { useState } from 'react';
import apiService from '../../../Service/apiService.jsx';
import './LoginPage.css';

export const LoginPage = ({ onLogin, navigate }) => {
  const [error, setError] = useState('');
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    // NOTE: Spring Security's formLogin expects form data, not JSON.
    // We create a URLSearchParams object to send the data correctly.
    const credentials = new URLSearchParams();
    credentials.append('username', e.target.email.value); // Spring Security expects 'username'
    credentials.append('password', e.target.password.value);

    try {
      await apiService.login(credentials); 
      onLogin();
    } catch (err) {
      setError('Login failed. Please check your credentials.');
      console.error(err);
    }
  };

  return (
    <div className="auth-container">
      <form className="auth-form" onSubmit={handleSubmit}>
        <h2 className="auth-title">Welcome Back</h2>
        {error && <p className="auth-error">{error}</p>}
        <div className="input-group">
          <label className="input-label" htmlFor="email">Email</label>
          <input className="input-field" type="email" id="email" name="email" required />
        </div>
        <div className="input-group">
          <label className="input-label" htmlFor="password">Password</label>
          <input className="input-field" type="password" id="password" name="password" required />
        </div>
        <button type="submit" className="auth-button">Login</button>
        <p className="auth-switch">
          Don't have an account?{' '}
          <span onClick={() => navigate('signup')} className="auth-switch-link">
            Sign Up
          </span>
        </p>
      </form>
    </div>
  );
};