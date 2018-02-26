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
    myReports: {
      all: [],
      total: 0,
      page: 0,
      next: '',
      previous: '',
    },
    myThemes: {},
  },

  getters: {
    getUserData: state => state.userData,
    userIsMapper: state => state.userData.is_mapper,
    userIsLogged: state => state.isLogged,
    getMyReports: state => state.myReports.all,
    getMyThemes: state => state.myThemes,
    myReportsTotal: state => state.myReports.total,
    myReportsPagination: state => Math.ceil(state.myReports.total / 10),
    myReportsNextUrl: state => state.myReports.next,
    myReportsPreviousUrl: state => state.myReports.previous,
    myReportsCurrentPage: state => state.myReports.page,
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
      state.myReports.all = obj.results;
      state.myReports.total = obj.count;
      state.myReports.next = (obj.next ? obj.next : '');
      state.myReports.previous = (obj.previous ? obj.previous : '');
    },

    [TYPES.SET_USER_THEMES](state, obj) {
      state.myThemes = obj;
    },

    [TYPES.SET_USER_REPORTS_PAGE](state, obj) {
      state.myReports.page = obj;
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

      let queryString = '';
      let currentPage = 1;

      if (obj && obj.page) {
        queryString = `&page=${obj.page}`;
        currentPage = obj.page;
      }

      const data = await axios.get(`/api/reports/?mapper=${user[0].id}&status=${obj.status}&project=${project.id}&page_size=10${queryString}`);
      commit(TYPES.SET_USER_REPORTS, data);
      commit(TYPES.SET_USER_REPORTS_PAGE, currentPage);
      return data.results;
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

      return new Promise((resolve, reject) => {
        axios.post('/api/users/', {
          username: obj.username,
          password: obj.password,
          email: obj.email,
          first_name: obj.name,
          avatar: 1,
        }).then(() => {
          dispatch('notifyOpen', { type: 1, message: 'Register successful!' });
          resolve();
        }).catch((error) => {
          let msg = '';

          if (error.response.data.non_field_errors) {
            msg = error.response.data.non_field_errors[0];
          }

          if (error.response.data.email) {
            msg = error.response.data.email[0];
          }

          dispatch('notifyOpen', { type: 0, message: msg });
          reject();
        });
      });
    },

    getMyThemesByProject: async ({ commit }) => {
      const project = helper.getItem('project');
      const user = helper.getItem('user');
      if (project && user) {
        const data = await axios.get(`/api/themes/?user=${user[0].id}&project=${project.id}`);
        commit(TYPES.SET_USER_THEMES, data);
      }
    },
  },
};
