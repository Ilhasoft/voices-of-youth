import axios from 'axios';
// import axios from '../config';
import * as TYPES from './types';

export default {
  state: {
    all: [],
    current: {},
    disclaimer: true,
  },

  getters: {
    getAllProjects: state => state.all,
    getCurrentProject: state => state.current,
    getDisclaimerProject: state => state.disclaimer,
  },

  /* eslint-disable no-param-reassign */
  mutations: {
    [TYPES.SET_PROJECTS_LIST](state, obj) {
      state.all = obj;
    },

    [TYPES.SET_CURRENT_PROJECT](state, obj) {
      state.current = obj;
      document.title = `Voices of Youth - ${obj.name}`;
    },

    [TYPES.SET_DISCLAIMER_PROJECT](state, obj) {
      state.disclaimer = obj;
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
      if (obj) {
        commit(TYPES.SET_CURRENT_PROJECT, obj);
        localStorage.setItem('project', JSON.stringify(obj));
      } else {
        commit(TYPES.SET_CURRENT_PROJECT, JSON.parse(localStorage.getItem('project')));
      }
    },

    showDisclaimerProject({ commit }, obj) {
      commit(TYPES.SET_DISCLAIMER_PROJECT, obj);
    },
  },
};
