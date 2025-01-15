import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:5000' // Backend URL
});

export const login = async (email, password) => {
  const response = await API.post('/auth/login', { email, password });
  return response.data;
};

// Add other API functions as needed