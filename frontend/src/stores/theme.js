import axios from 'axios';
import * as TYPES from './types';
import helper from '../helper';

const language = helper.getItem('language');
const query = language ? `&lang=${language}` : '';

export default {
  state: {
    all: [],
    dateFrom: '',
    dateTo: '',
    theme: {},
  },

  getters: {
    getThemes: state => state.all,
    getTheme: state => state.theme,
  },

  /* eslint-disable no-param-reassign */
  mutations: {
    [TYPES.SET_THEMES](state, obj) {
      state.all = obj;
    },

    [TYPES.SET_CURRENT_THEME](state, obj) {
      state.theme = obj;
    },
  },

  actions: {
    getThemes({ commit }) {
      const project = helper.getItem('project');
      axios.get(`/api/themes?project=${project.id}${query}`).then((response) => {
        commit(TYPES.SET_THEMES, response.data);
      }).catch((error) => {
        throw new Error(error);
      });
    },

    getTheme({ commit }, obj) {
      const project = helper.getItem('project');
      axios.get(`/api/themes/${obj}?project=${project.id}${query}`).then((response) => {
        commit(TYPES.SET_CURRENT_THEME, response.data);
      }).catch((error) => {
        throw new Error(error);
      });
    },
  },
};
