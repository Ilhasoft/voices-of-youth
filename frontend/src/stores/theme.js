import axios from 'axios';
import helper from '@/helper';
import * as TYPES from './types';

const language = helper.getItem('language');
const query = language ? `&lang=${language}` : '';

export default {
  state: {
    all: [],
    dateFrom: '',
    dateTo: '',
    theme: {},
    lastReports: [],
  },

  getters: {
    getThemes: state => state.all,
    getTheme: state => state.theme,
    getLastReports: state => state.lastReports,
  },

  /* eslint-disable no-param-reassign */
  mutations: {
    [TYPES.SET_THEMES](state, obj) {
      state.all = obj;
    },

    [TYPES.SET_CURRENT_THEME](state, obj) {
      state.theme = obj;
    },

    [TYPES.SET_LAST_REPORTS](state, obj) {
      state.lastReports = obj.filter(item => item.last_image !== null);
    },
  },

  actions: {
    getThemes: async ({ commit, dispatch }, obj) => {
      const project = helper.getItem('project');
      let queryYear = '';

      if (obj && (obj.yearStart && obj.yearEnd)) {
        queryYear = `&year-start=${obj.yearStart}&year-end=${obj.yearEnd}`;
      }

      const data = await axios.get(`/api/themes?project=${project.id}${query}${queryYear}`);
      commit(TYPES.SET_THEMES, data);
    },

    getTheme: async ({ commit, dispatch }, obj) => {
      commit(TYPES.SET_CURRENT_THEME, {});
      commit(TYPES.SET_LAST_REPORTS, []);

      const project = helper.getItem('project');
      const data = await axios.get(`/api/themes/${obj}?project=${project.id}${query}`);
      commit(TYPES.SET_CURRENT_THEME, data);

      const last = await axios.get(`/api/reports/?project=${project.id}&theme=${obj}&page_size=10`);
      commit(TYPES.SET_LAST_REPORTS, last.results);
    },
  },
};
