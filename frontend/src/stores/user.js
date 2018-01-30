import axios from 'axios';
import * as TYPES from './types';
import helper from '../helper';

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
      const project = helper.getItem('project');
      return axios.get(`/api/reports/?mapper=${user[0].id}&status=${obj}&project=${project.id}`).then((response) => {
        commit(TYPES.SET_USER_REPORTS, response.data);
        return response.data;
      }).catch(() => {
        dispatch('notifyOpen', { type: 0, message: 'Error, try again' });
      });
    },

    executeUpdateProfile({ commit, dispatch }, obj) {
      const user = helper.getItem('user');
      const token = helper.getItem('token');
      return axios.put(`/api/users/${user[0].id}/`, {
        email: obj.email,
        first_name: obj.name,
      }, {
        headers: { authorization: `Token ${token}` },
      }).then(() => {
        axios.get(`/api/users/?auth_token=${token}`).then((response) => {
          helper.setItem('user', response.data);
          dispatch('setCurrentUser');
          dispatch('notifyOpen', { type: 1, message: 'Profile updated!' });
        });
      }).catch(() => {
        dispatch('notifyOpen', { type: 0, message: 'Error, try again' });
      });
    },

    executeUpdatePassword({ commit, dispatch }, obj) {
      const user = helper.getItem('user');
      const token = helper.getItem('token');
      return axios.put(`/api/users/${user[0].id}/`, {
        password: obj,
      }, {
        headers: { authorization: `Token ${token}` },
      });
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
