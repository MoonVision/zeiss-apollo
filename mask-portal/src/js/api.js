import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
  headers: {'Access-Control-Allow-Origin': '*'},
});


export default {
  get: (...params) => {
    return api.get(...params);
  },
  post: (...params) => {
    return api.get(...params);
  },
};