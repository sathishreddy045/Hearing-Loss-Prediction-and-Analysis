// src/Service/apiService.jsx
import axios from 'axios';

// Create an instance of axios with a base URL.
const apiClient = axios.create({
  baseURL: 'http://localhost:8080/api',
  // This tells axios to send cookies received from the backend with every request.
  withCredentials: true, 
});

const apiService = {
  // --- Authentication ---
  signup(userData) {
    // Signup still uses the default JSON content type
    return apiClient.post('/auth/signup', userData);
  },

  // UPDATED: The login function now sends data in the correct format
  login(credentials) {
    return apiClient.post('/auth/login', credentials, {
      // This header is required by Spring Security's formLogin
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
  },

  logout() {
    return apiClient.post('/auth/logout');
  },

  // --- Prediction ---
  // This will continue to use the default JSON content type
  getPrediction(formData) {
    return apiClient.post('/predict', formData);
  },
};

export default apiService;
