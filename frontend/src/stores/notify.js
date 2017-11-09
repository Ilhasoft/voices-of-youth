import * as TYPES from './types';

export default {
  state: {
    message: '',
    visible: false,
    type: 0,
  },

  getters: {
    getNotifyInfo: state => state,
  },

  /* eslint-disable no-param-reassign */
  mutations: {
    [TYPES.NOTIFY_SET_INFO](state, obj) {
      state.visible = obj.visible;

      if (obj.message) {
        state.visible = true;
        state.message = obj.message;
      }

      if (obj.type) {
        state.type = obj.type;
      }
    },
  },

  actions: {
    notifyOpen({ commit }, obj) {
      commit(TYPES.NOTIFY_SET_INFO, obj);
    },

    notifyClose({ commit }) {
      commit(TYPES.NOTIFY_SET_INFO, { visible: false });
    },
  },
};
