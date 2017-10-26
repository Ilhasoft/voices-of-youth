import axios from 'axios';
import * as TYPES from './types';
import helper from '../helper';

export default {
  state: {
    all: [],
    report: {},
  },

  getters: {
    getReports: state => state.all,
    getReport: state => state.report,
  },

  /* eslint-disable no-param-reassign */
  mutations: {
    [TYPES.SET_REPORTS](state, obj) {
      state.all = obj;
    },

    [TYPES.SET_CURRENT_REPORT](state, obj) {
      state.theme = obj;
    },

    [TYPES.ADD_REPORTS_LIST](state, obj) {
      state.theme = obj;
    },

    [TYPES.REMOVE_REPORTS_LIST](state, obj) {
      state.theme = obj;
    },
  },

  actions: {
    getReports({ commit }, obj) {
      let query = '';

      if (obj) {
        query = `theme_id=${obj.theme}`;
      } else {
        const project = helper.getItem('project');
        query = `project_id=${project.id}`;
      }

      axios.get(`/api/reports?${query}`).then((response) => {
        commit(TYPES.SET_REPORTS, response.data);
      }).catch((error) => {
        throw new Error(error);
      });
    },

    getReportsByTheme({ commit }, obj) {
      if (obj.isChecked) {
        axios.get(`/api/reports?theme_id=${obj.themeId}`).then((response) => {
          commit(TYPES.ADD_REPORTS_LIST, response.data);
        }).catch((error) => {
          throw new Error(error);
        });
      } else {
        commit(TYPES.REMOVE_REPORTS_LIST, obj.themeId);
      }
    },

    getReport({ commit }, obj) {
      axios.get(`/api/reports/${obj}`).then((response) => {
        commit(TYPES.SET_CURRENT_REPORT, response.data);
      }).catch((error) => {
        throw new Error(error);
      });
    },
  },
};
