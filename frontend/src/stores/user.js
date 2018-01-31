import axios from 'axios';
import helper from '@/helper';
import * as TYPES from './types';

export default {
  state: {
    userData: {
      id: 0,
      first_name: '',
      last_name: '',
      username: '',
      avatar: '',
      email: '',
      is_admin: false,
      is_mapper: false,
      language: '',
    },
    isLogged: false,
    loginError: {},
    myReports: {},
  },

  getters: {
    getUserData: state => state.userData,
    userIsMapper: state => state.userData.is_mapper,
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

    executeLogin: async ({ commit }, obj) => {
      const data = await axios.post('/api/get_auth_token/', {
        username: obj.username,
        password: obj.password,
      });

      const token = data.token;
      helper.setItem('token', token);

      const user = await axios.get(`/api/users/?auth_token=${token}`);
      helper.setItem('user', user);

      return data;
    },

    executeLogout({ commit }) {
      helper.setItem('user', '');
      helper.setItem('token', '');
      return commit(TYPES.SET_USER_DATA, {
        userData: {},
        isLogged: false,
      });
    },

    myReports: async ({ commit, dispatch }, obj) => {
      const user = helper.getItem('user');
      const project = helper.getItem('project');
      const data = await axios.get(`/api/reports/?mapper=${user[0].id}&status=${obj}&project=${project.id}`);
      commit(TYPES.SET_USER_REPORTS, data);
      return data;
    },

    executeUpdateProfile: async ({ commit, dispatch }, obj) => {
      const user = helper.getItem('user');
      await axios.put(`/api/users/${user[0].id}/`, {
        email: obj.email,
        first_name: obj.name,
      });

      const auth = await axios.get(`/api/users/?auth_token=${helper.getItem('token')}`);
      helper.setItem('user', auth);
      dispatch('setCurrentUser');
      dispatch('notifyOpen', { type: 1, message: 'Profile updated!' });
    },

    executeUpdatePassword: async ({ commit, dispatch }, obj) => {
      const user = helper.getItem('user');
      await axios.put(`/api/users/${user[0].id}/`, { password: obj });
    },

    executeRegisterProfile({ commit, dispatch }, obj) {
      if (!obj.name || !obj.email || !obj.username || !obj.password) {
        dispatch('notifyOpen', { type: 0, message: 'All fields are required!' });
        return false;
      } else if (obj.password && obj.confirmPassword && obj.password !== obj.confirmPassword) {
        dispatch('notifyOpen', { type: 0, message: 'Password not match!' });
        return false;
      }

      return axios.post('/api/users/', {
        username: obj.username,
        password: obj.password,
        email: obj.email,
        first_name: obj.name,
        avatar: 1,
      }).then(() => {
        dispatch('notifyOpen', { type: 1, message: 'Register successful!' });
      }).catch(() => {
        dispatch('notifyOpen', { type: 0, message: 'Error, try again' });
      });
    },
  },
};
