export default {
  state: {
    userData: {},
    isLogged: false,
  },

  getters: {
    getUserData: state => state.userData,
    userIsLogged: state => state.isLogged,
  },
};
