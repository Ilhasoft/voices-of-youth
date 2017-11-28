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

  formatDate(createdOn) {
    const date = new Date(createdOn);
    return `${date.toLocaleString('en-us', { month: 'short' })} ${date.getDate()}, ${date.getFullYear()}`;
  },
};
