// src/api/index.js
import axios from 'axios';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Global error handler for API requests
 * @param {Error} error - The error object from axios
 * @returns {Promise} - Rejected promise with error details
 */
export const handleApiError = (error) => {
  console.error('API Error:', error);
  
  // Handle different types of errors
  if (error.response) {
    // The request was made and the server responded with a status code
    // that falls out of the range of 2xx
    console.error('Response error:', error.response.data);
    return Promise.reject({
      status: error.response.status,
      data: error.response.data
    });
  } else if (error.request) {
    // The request was made but no response was received
    console.error('Request error - no response received');
    return Promise.reject({
      status: 0,
      message: 'No response received from server'
    });
  } else {
    // Something else caused the error
    console.error('Error setting up request:', error.message);
    return Promise.reject({
      message: error.message
    });
  }
};

export default apiClient;