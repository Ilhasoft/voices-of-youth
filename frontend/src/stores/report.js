import axios from 'axios';
import L from 'leaflet';
import helper from '@/helper';
import * as TYPES from './types';

export default {
  state: {
    all: [],
    report: {},
    themes: [],
    comments: [],
    files: [],
    search: [],
  },

  getters: {
    getReports: state => state.all,
    getReport: state => state.report,
    getComments: state => state.comments,
    getReportFiles: state => state.files,
    getReportUrls: state => state.urls,
    getUserThemes: state => state.themes,
    getReportPreview: state => state.files,
    getSearchReports: state => state.search,
    getReportsPins: (state) => {
      const markers = [];

      if (state.all.length > 0) {
        const LeafIcon = L.Icon.extend({
          options: {
            shadowUrl: '',
            iconSize: [25, 38],
            iconAnchor: [18, 34],
          },
        });

        state.all.map((report) => {
          const tempIcon = new LeafIcon({ iconUrl: report.pin });

          markers.push({
            id: report.id,
            latlng: L.latLng(report.location.coordinates[1], report.location.coordinates[0]),
            text: report.text,
            color: report.theme_color,
            icon: tempIcon,
          });

          return true;
        });
      }
      return markers;
    },
  },

  /* eslint-disable no-param-reassign */
  mutations: {
    [TYPES.SET_REPORTS](state, obj) {
      state.all = [];
      state.themes = [];
      state.all = obj;
    },

    [TYPES.SET_CURRENT_REPORT](state, obj) {
      state.report = obj;
    },

    [TYPES.ADD_REPORTS_LIST](state, obj) {
      Object.keys(obj.reports).map((key, index) => {
        state.all.push(obj.reports[index]);
        return true;
      });
    },

    [TYPES.REMOVE_REPORTS_LIST](state, obj) {
      state.all = state.all.filter(item => item.theme !== obj.theme);
    },

    [TYPES.SET_REPORT_COMMENTS](state, obj) {
      state.comments = obj;
    },

    [TYPES.SET_REPORT_MEDIAS](state, obj) {
      state.files = obj;
    },

    [TYPES.CLEAR_REPORTS_LIST](state) {
      state.all = [];
      state.themes = [];
    },

    [TYPES.REMOVE_COMMENT](state, obj) {
      state.comments = state.comments.filter(item => item.id !== obj);
    },

    [TYPES.NEW_REPORT_USER_THEMES](state, obj) {
      state.themes = obj;
    },

    [TYPES.SET_REPORTS_SEARCH](state, obj) {
      state.search = obj;
    },
  },

  actions: {
    getReports: async ({ commit }) => {
      const project = helper.getItem('project');
      const data = await axios.get(`/api/reports?project=${project.id}&status=1`);
      commit(TYPES.SET_REPORTS, data);
    },

    getReportsByTheme: async ({ dispatch, commit, state }, obj) => {
      if (obj.isChecked) {
        const data = await axios.get(`/api/reports?theme=${obj.themeId}&status=1`);
        commit(TYPES.ADD_REPORTS_LIST, { reports: data, theme: obj.themeId });
      } else {
        commit(TYPES.REMOVE_REPORTS_LIST, { theme: obj.themeId });
      }
    },

    getReport: async ({ commit, dispatch }, obj) => {
      commit(TYPES.SET_CURRENT_REPORT, {});
      commit(TYPES.SET_REPORT_MEDIAS, {});

      const data = await axios.get(`/api/reports/${obj}/`);
      commit(TYPES.SET_CURRENT_REPORT, data);

      const files = await axios.get(`/api/report-files/?report=${obj}`);
      commit(TYPES.SET_REPORT_MEDIAS, files.results);
    },

    cleanReport: ({ commit }) => {
      commit(TYPES.SET_CURRENT_REPORT, {});
    },

    getComments: async ({ commit, dispatch }, obj) => {
      const data = await axios.get(`/api/report-comments/?report=${obj}`);
      commit(TYPES.SET_REPORT_COMMENTS, data);
    },

    clearReports({ commit }) {
      commit(TYPES.CLEAR_REPORTS_LIST);
    },

    saveNewComment: async ({ commit, dispatch }, obj) => {
      await axios.post('/api/report-comments/', {
        text: obj.text,
        report: obj.report,
      }).then(() => {
        dispatch('notifyOpen', { type: 1, message: 'Comment Sent!' });
      }).catch(() => {
        dispatch('notifyOpen', { type: 0, message: 'Error, try again.' });
      });
    },

    deleteComment: async ({ commit, dispatch }, obj) => {
      await axios.delete(`/api/report-comments/${obj}/`).then(() => {
        commit(TYPES.REMOVE_COMMENT, obj);
        dispatch('notifyOpen', { type: 1, message: 'Comment Removed!' });
      }).catch((error) => {
        dispatch('notifyOpen', { type: 0, message: 'Error, try again.' });
        throw new Error(error);
      });
    },

    getUserThemes: async ({ commit }, obj) => {
      const project = helper.getItem('project');
      const data = await axios.get(`/api/themes/?user=${obj}&project=${project.id}`);
      commit(TYPES.NEW_REPORT_USER_THEMES, data);
    },

    getProjectThemes: async ({ commit }) => {
      const project = helper.getItem('project');
      const data = await axios.get(`/api/themes?project=${project.id}`);
      commit(TYPES.NEW_REPORT_USER_THEMES, data);
    },

    getUsersByTheme: async ({ commit }, obj) => {
      await axios.get(`/api/users?theme=${obj}`);
    },

    saveNewReport: async ({ commit, dispatch }, obj) => {
      const data = await axios.post('/api/reports/', obj)
      .then()
      .catch((error) => {
        let messageError = '';
        const json = JSON.parse(error.response.request.responseText);

        if (json.location) {
          messageError = json.location[0];
        }

        if (json.detail) {
          messageError = json.detail;
        }

        if (json.non_field_errors) {
          messageError = json.non_field_errors[0];
        }

        dispatch('notifyOpen', { type: 0, message: messageError });
        throw new Error(error);
      });

      return data;
    },

    saveEditReport: async ({ commit, dispatch }, obj) => {
      const data = await axios.put(`/api/reports/${obj.id}/`, obj)
      .then()
      .catch((error) => {
        let messageError = '';
        const json = JSON.parse(error.response.request.responseText);

        if (json.location) {
          messageError = json.location[0];
        }

        if (json.detail) {
          messageError = json.detail;
        }

        if (json.non_field_errors) {
          messageError = json.non_field_errors[0];
        }

        dispatch('notifyOpen', { type: 0, message: messageError });
        throw new Error(error);
      });

      return data;
    },

    saveFiles: async ({ commit }, obj) => {
      const form = new FormData();
      form.append('file', obj.file);
      form.append('title', obj.file.name);
      form.append('description', obj.file.name);
      form.append('report_id', obj.id);

      const data = await axios.post('/api/report-files/', form, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return data;
    },

    removeFiles: async ({ commit }, obj) => {
      await axios.delete(`/api/report-files/${obj}/`);
    },

    searchReports: async ({ commit, dispatch }, obj) => {
      const project = helper.getItem('project');
      const data = await axios.get(`/api/report-search/?query=${obj}&project=${project.id}`);
      commit(TYPES.SET_REPORTS_SEARCH, data);
    },
  },
};
