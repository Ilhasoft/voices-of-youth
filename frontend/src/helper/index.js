export default {
  setItem(name, value) {
    window.localStorage.setItem(name, JSON.stringify(value));
  },

  getItem(name) {
    const item = window.localStorage.getItem(name);
    if (item) {
      return JSON.parse(item);
    }
    return '';
  },
};
