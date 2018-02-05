import axios from 'axios';
import * as TYPES from './types';

export default {
  state: {
    menuTitle: '',
    showMenu: true,
    selectProjects: true,
    showSearch: true,
    showNotification: true,
    showAccount: true,
    showNewReport: true,
    showBackButton: false,
    notifications: [],
  },

  getters: {
    menuIsVisibled: state => state.showMenu,
    menuTitle: state => state.menuTitle,
    menuNewReport: state => state.showNewReport,
    menuProjectsVisibled: state => state.selectProjects,
    menuBackVisibled: state => state.showBackButton,
    getNotifications: state => state.notifications,
  },

  /* eslint-disable no-param-reassign */
  mutations: {
    [TYPES.SET_HEADER_CONFIG](state, obj) {
      if (obj.menuTitle) state.menuTitle = obj.menuTitle;
      if (obj.showMenu !== undefined) state.showMenu = obj.showMenu;
      if (obj.showProjects !== undefined) state.selectProjects = obj.showProjects;
      if (obj.showBackButton !== undefined) state.showBackButton = obj.showBackButton;
    },

    [TYPES.SET_NOTIFICATIONS](state, obj) {
      state.notifications = obj;
    },
  },

  actions: {
    updateHeaderConfig({ commit, state }, obj) {
      commit(TYPES.SET_HEADER_CONFIG, obj);
    },

    getNotifications: async ({ commit }) => {
      const data = await axios.get('/api/report-notification');
      commit(TYPES.SET_NOTIFICATIONS, data);
    },

    setNotificationRead: async ({ dispatch }, obj) => {
      await axios.put(`/api/report-notification/${obj}/`);
      dispatch('getNotifications');
    },
  },
};
