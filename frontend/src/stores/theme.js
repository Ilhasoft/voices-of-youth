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
    getThemes({ commit, dispatch }, obj) {
      const project = helper.getItem('project');
      let queryYear = '';

      if (obj && (obj.yearStart && obj.yearEnd)) {
        queryYear = `&year-start=${obj.yearStart}&year-end=${obj.yearEnd}`;
      }

      axios.get(`/api/themes?project=${project.id}${query}${queryYear}`).then((response) => {
        commit(TYPES.SET_THEMES, response.data);
      }).catch((error) => {
        dispatch('notifyOpen', { type: 0, message: 'Error, try again.' });
        throw new Error(error);
      });
    },

    getTheme({ commit, dispatch }, obj) {
      const project = helper.getItem('project');
      axios.get(`/api/themes/${obj}?project=${project.id}${query}`).then((response) => {
        commit(TYPES.SET_CURRENT_THEME, response.data);
      }).then(() => {
        axios.get(`/api/reports/?project=${project.id}&theme=${obj}&page_size=10`).then((response) => {
          commit(TYPES.SET_LAST_REPORTS, response.data.results);
        }).catch(() => {
          dispatch('notifyOpen', { type: 0, message: 'Error, try again.' });
        });
      }).catch((error) => {
        dispatch('notifyOpen', { type: 0, message: 'Error, try again.' });
        throw new Error(error);
      });
    },
  },
};
