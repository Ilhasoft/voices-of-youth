import axios from 'axios';
import * as TYPES from './types';
import helper from '../helper';

export default {
  state: {
    userData: {},
    isLogged: false,
    loginError: {},
    myReports: {},
  },

  getters: {
    getUserData: state => state.userData,
    userIsLogged: state => state.isLogged,
    getMyReports: state => state.myReports,
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

    [TYPES.SET_USER_REPORTS](state, obj) {
      state.myReports = obj;
    },
  },

  actions: {
    setCurrentUser({ commit }) {
      const userData = helper.getItem('user');
      if (userData) {
        commit(TYPES.SET_USER_DATA, {
          userData: userData[0],
          isLogged: true,
        });
      }
    },

    executeLogin({ commit, dispatch }, obj) {
      return axios.post('/api/get_auth_token/', {
        username: obj.username,
        password: obj.password,
      }).then((response) => {
        const token = response.data.token;
        helper.setItem('token', token);
        return token;
      }).then((token) => {
        const user = axios.get(`/api/users/?auth_token=${token}`).then((response) => {
          helper.setItem('user', response.data);
          return response.data;
        });
        return user;
      }).catch((error) => {
        dispatch('notifyOpen', { type: 0, message: error.response.data.non_field_errors[0] });
      });
    },

    executeLogout({ commit }) {
      helper.setItem('user', '');
      helper.setItem('token', '');
      return commit(TYPES.SET_USER_DATA, {
        userData: {},
        isLogged: false,
      });
    },

    myReports({ commit, dispatch }, obj) {
      const user = helper.getItem('user');
      axios.get(`/api/reports/?mapper=${user[0].id}&status=${obj}`).then((response) => {
        commit(TYPES.SET_USER_REPORTS, response.data);
      }).catch(() => {
        dispatch('notifyOpen', { type: 0, message: 'Error, try again' });
      });
    },
  },
};
