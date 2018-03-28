import axios from 'axios';
import helper from '@/helper';
import * as TYPES from './types';

export default {
  state: {
    all: [],
    current: {},
    language: '',
    disclaimer: true,
  },

  getters: {
    getAllProjects: state => state.all,
    getCurrentProject: state => state.current,
    getDisclaimerProject: state => state.disclaimer,
    getProjectLanguages: state => state.current.languages,
    getCurrentLanguage: state => state.language,
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

    [TYPES.SET_CURRENT_LANGUAGE](state, obj) {
      state.language = obj;
    },
  },

  actions: {
    setProjects: async ({ commit }) => {
      const data = await axios.get('/api/projects', {
        headers: {
          Authorization: '',
        },
      });
      commit(TYPES.SET_PROJECTS_LIST, data);
    },

    setCurrentProject: async ({ commit, state }, obj) => {
      if (obj.id !== undefined) {
        commit(TYPES.SET_CURRENT_PROJECT, obj);
        localStorage.setItem('project', JSON.stringify(obj));
      } else {
        const project = JSON.parse(localStorage.getItem('project'));
        if (project) {
          commit(TYPES.SET_CURRENT_PROJECT, JSON.parse(localStorage.getItem('project')));
        } else {
          const data = await axios.get('/api/projects');
          const response = data.filter(item => item.path === obj.path)[0];

          localStorage.setItem('project', JSON.stringify(response));
          commit(TYPES.SET_CURRENT_PROJECT, response);
        }
      }
    },

    showDisclaimerProject({ commit }, obj) {
      commit(TYPES.SET_DISCLAIMER_PROJECT, obj);
    },

    setCurrentLanguage: async ({ commit, state, dispatch }, obj) => {
      if (obj) {
        const project = helper.getItem('project');
        const data = await axios.get(`/api/projects/${project.id}/?lang=${obj}`);
        localStorage.setItem('project', JSON.stringify(data));
        localStorage.setItem('language', JSON.stringify(obj));
        window.location.reload();
      }
    },
  },
};
