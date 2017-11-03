import axios from 'axios';
import * as TYPES from './types';

export default {
  state: {
    userData: {},
    isLogged: false,
    loginError: {},
  },

  getters: {
    getUserData: state => state.userData,
    userIsLogged: state => state.isLogged,
  },

  /* eslint-disable no-param-reassign */
  mutations: {
    [TYPES.SET_LOGIN_ERROR](state, obj) {
      state.loginError = obj;
    },

    [TYPES.SET_USER_DATA](state, obj) {
      state.userData = obj.userData;
      state.isLogged = obj.isLogged;
    },
  },

  actions: {
    setCurrentUser({ commit }) {
      const userData = JSON.parse(localStorage.getItem('user'));
      if (userData) {
        commit(TYPES.SET_USER_DATA, {
          userData: userData[0],
          isLogged: true,
        });
      }
    },

    executeLogin({ commit }, obj) {
      return axios.post('/api/get_auth_token/', {
        username: obj.username,
        password: obj.password,
      }).then((response) => {
        const token = response.data.token;
        localStorage.setItem('token', JSON.stringify(token));
        return token;
      }).then((token) => {
        const user = axios.get(`/api/users/?auth_token=${token}`).then((response) => {
          localStorage.setItem('user', JSON.stringify(response.data));
          return response.data;
        });
        return user;
      }).catch((error) => {
        commit(TYPES.SET_LOGIN_ERROR, error.message);
        return error.message;
      });
    },

    executeLogout({ commit }) {
      commit(TYPES.SET_USER_DATA, {
        userData: {},
        isLogged: false,
      });
    },
  },
};
