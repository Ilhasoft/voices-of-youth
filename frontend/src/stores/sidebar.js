import * as TYPES from './types';

export default {
  state: {
    isActived: false,
    tabActived: '',
  },

  getters: {
    getSideBarIsActived: state => state.isActived,
    getSideBarConfig: state => state,
  },

  /* eslint-disable no-param-reassign */
  mutations: {
    [TYPES.SIDEBAR_SET_CONFIGS](state, obj) {
      state.isActived = obj.isActived;
      state.tabActived = obj.tabActived;
    },
  },

  actions: {
    setSideBarConfigs({ commit, state }, obj) {
      commit(TYPES.SIDEBAR_SET_CONFIGS, obj);
    },
  },
};
