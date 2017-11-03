export default {
  urlAPI: 'http://localhost:8000/api/',

  setItem(name, value) {
    window.localStorage.setItem(name, JSON.stringify(value));
  },

  getItem(name) {
    return JSON.parse(window.localStorage.getItem(name));
  },
};
