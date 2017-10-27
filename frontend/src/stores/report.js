import axios from 'axios';
import * as TYPES from './types';
import helper from '../helper';

export default {
  state: {
    all: [],
    report: {},
    themes: [],
    comments: [],
    files: [],
    urls: [],
  },

  getters: {
    getReports: state => state.all,
    getReport: state => state.report,
    getComments: state => state.comments,
    getReportFiles: state => state.files,
    getReportUrls: state => state.urls,
  },

  /* eslint-disable no-param-reassign */
  mutations: {
    [TYPES.SET_REPORTS](state, obj) {
      state.all = obj;
    },

    [TYPES.SET_CURRENT_REPORT](state, obj) {
      state.report = obj;
    },

    [TYPES.ADD_REPORTS_LIST](state, obj) {
      if (state.themes.length === 0) {
        state.all = [];
        state.all = obj.data;
      } else {
        Object.keys(obj.data).map((key, index) => {
          state.all.push(obj.data[index]);
          return true;
        });
      }

      state.themes.push(obj.theme);
    },

    [TYPES.REMOVE_REPORTS_LIST](state, obj) {
      const index = state.themes.indexOf(obj.theme);
      if (index !== -1) {
        state.themes.splice(index, 1);
        state.all = state.all.filter(item => item.theme_id !== obj.theme);
      }
    },

    [TYPES.SET_REPORT_COMMENTS](state, obj) {
      state.comments = obj;
    },

    [TYPES.SET_REPORT_MEDIAS](state, obj) {
      state.files = obj.files;
      state.urls = obj.urls;
    },
  },

  actions: {
    getReports({ commit }) {
      const project = helper.getItem('project');
      axios.get(`/api/reports?project=${project.id}`).then((response) => {
        commit(TYPES.SET_REPORTS, response.data);
      }).catch((error) => {
        throw new Error(error);
      });
    },

    getReportsByTheme({ dispatch, commit, state }, obj) {
      if (obj.isChecked) {
        axios.get(`/api/reports?theme=${obj.themeId}`).then((response) => {
          commit(TYPES.ADD_REPORTS_LIST, {
            data: response.data,
            theme: obj.themeId,
          });
        }).catch((error) => {
          throw new Error(error);
        });
      } else {
        commit(TYPES.REMOVE_REPORTS_LIST, {
          theme: obj.themeId,
        });

        if (state.themes.length === 0) {
          dispatch('getReports');
        }
      }
    },

    getReport({ commit }, obj) {
      axios.get(`/api/reports/${obj}`).then((response) => {
        commit(TYPES.SET_CURRENT_REPORT, response.data);
      }).then(() => {
        axios.get(`/api/report-medias/?report=${obj}`).then((response) => {
          commit(TYPES.SET_REPORT_MEDIAS, response.data[0]);
        });
      }).catch((error) => {
        throw new Error(error);
      });
    },

    getComments({ commit }, obj) {
      axios.get(`/api/report-comments/?report=${obj}`).then((response) => {
        commit(TYPES.SET_REPORT_COMMENTS, response.data);
      }).catch((error) => {
        throw new Error(error);
      });
    },
  },
};
