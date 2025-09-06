import React, { useState } from 'react';
import apiService from '../../../Service/apiService'; // Import the apiService
import './SignupPage.css';

export const SignupPage = ({ onSignup, navigate }) => {
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    const userData = {
      fullName: e.target.name.value,
      email: e.target.email.value,
      password: e.target.password.value,
    };

    try {
      const response = await apiService.signup(userData);
      console.log('Signup successful:', response.data);
      onSignup(); // This will log the user in
    } catch (err) {
      setError(err.response?.data || 'An error occurred during signup.');
      console.error(err);
    }
  };

  return (
    <div className="auth-container">
      <form className="auth-form" onSubmit={handleSubmit}>
        <h2 className="auth-title">Create Account</h2>
        {error && <p className="auth-error">{error}</p>}
        {/* ... form inputs ... */}
        <div className="input-group">
            <label className="input-label" htmlFor="name">Full Name</label>
            <input className="input-field" type="text" id="name" name="name" required />
        </div>
        <div className="input-group">
            <label className="input-label" htmlFor="signup-email">Email</label>
            <input className="input-field" type="email" id="signup-email" name="email" required />
        </div>
        <div className="input-group">
            <label className="input-label" htmlFor="signup-password">Password</label>
            <input className="input-field" type="password" id="signup-password" name="password" required />
        </div>
        <button type="submit" className="auth-button">Sign Up</button>
        <p className="auth-switch">
          Already have an account?{' '}
          <span onClick={() => navigate('login')} className="auth-switch-link">
            Login
          </span>
        </p>
      </form>
    </div>
  );
};
