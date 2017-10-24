import * as TYPES from './types';

export default {
  state: {
    isActived: false,
    title: '',
    tabActived: '',
    backButton: true,
    backTo: '',
  },

  getters: {
    getSideBarIsActived: state => state.isActived,
    getSideBarConfig: state => state,
  },

  /* eslint-disable no-param-reassign */
  mutations: {
    [TYPES.SIDEBAR_SET_CONFIGS](state, obj) {
      state.isActived = obj.isActived;
      state.title = obj.title;
      state.tabActived = obj.tabActived;
      state.backButton = obj.backButton;
      state.backTo = obj.backTo;
    },

    [TYPES.SIDEBAR_SET_CURRENT_TAB](state, obj) {
      state.tabActived = obj;
    },
  },

  actions: {
    setSideBarConfigs({ commit, state }, obj) {
      commit(TYPES.SIDEBAR_SET_CONFIGS, obj);
    },

    sideBarBackTo({ commit, state }, obj) {
      commit(TYPES.SIDEBAR_SET_CURRENT_TAB, obj);
    },
  },
};
