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
  },

  getters: {
    menuIsVisibled: state => state.showMenu,
    menuTitle: state => state.menuTitle,
    menuNewReport: state => state.showNewReport,
    menuProjectsVisibled: state => state.selectProjects,
    menuBackVisibled: state => state.showBackButton,
  },

  /* eslint-disable no-param-reassign */
  mutations: {
    [TYPES.SET_HEADER_CONFIG](state, obj) {
      if (obj.menuTitle) state.menuTitle = obj.menuTitle;
      if (obj.showMenu !== undefined) state.showMenu = obj.showMenu;
      if (obj.showProjects !== undefined) state.selectProjects = obj.showProjects;
      if (obj.showBackButton !== undefined) state.showBackButton = obj.showBackButton;
    },
  },

  actions: {
    updateHeaderConfig({ commit, state }, obj) {
      commit(TYPES.SET_HEADER_CONFIG, obj);
    },
  },
};
