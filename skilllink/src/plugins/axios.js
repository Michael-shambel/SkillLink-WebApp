/**
 * A centralized configuration to handle all REST API calls
 */
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  }
});

export default apiClient;
