import axios from 'axios';
import * as TYPES from './types';

export default {
  state: {
    all: [],
    current: {},
  },

  getters: {
    getAllProjects: state => state.all,
    getCurrentProject: state => state.current,
  },

  /* eslint-disable no-param-reassign */
  mutations: {
    [TYPES.SET_PROJECTS_LIST](state, obj) {
      state.all = obj;
    },

    [TYPES.SET_CURRENT_PROJECT](state, obj) {
      state.current = obj;
    },
  },

  actions: {
    setProjects({ commit }) {
      axios.get('/api/projects').then((response) => {
        commit(TYPES.SET_PROJECTS_LIST, response.data);
      }).catch((error) => {
        throw new Error(error);
      });
    },

    setCurrentProject({ commit, state }, obj) {
      commit(TYPES.SET_CURRENT_PROJECT, obj);
    },
  },
};
