import axios from 'axios';
import L from 'leaflet';
import * as TYPES from './types';
import helper from '../helper';

const mapsKey = 'AIzaSyColv5Z7Xf-YiEPRO-eX4RSLzakAGYGNkw';

export default {
  state: {
    all: [],
    report: {},
    themes: [],
    comments: [],
    files: [],
    urls: [],
    newReport: {
      themes: [],
      title: '',
      description: '',
      tags: [],
      files: [],
      urls: [],
      location: {},
    },
  },

  getters: {
    getReports: state => state.all,
    getReport: state => state.report,
    getComments: state => state.comments,
    getReportFiles: state => state.files,
    getReportUrls: state => state.urls,
    getReportNewData: state => state.newReport,
    getReportPreview: state => state.files[0],
    getReportsPins: (state) => {
      const markers = [];

      if (state.all.length > 0) {
        const LeafIcon = L.Icon.extend({
          options: {
            shadowUrl: '',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
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
      if (state.themes.length === 0) {
        state.all = [];
        state.all = obj.data;
      } else if (state.themes.indexOf(obj.theme) === -1) {
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
        state.all = state.all.filter(item => item.theme !== obj.theme);
      }
    },

    [TYPES.SET_REPORT_COMMENTS](state, obj) {
      state.comments = obj;
    },

    [TYPES.SET_REPORT_MEDIAS](state, obj) {
      state.files = obj.files;
      state.urls = obj.urls;
    },

    [TYPES.CLEAR_REPORTS_LIST](state) {
      state.all = [];
      state.themes = [];
    },

    [TYPES.REMOVE_COMMENT](state, obj) {
      state.comments = state.comments.filter(item => item.id !== obj);
    },

    [TYPES.NEW_REPORT_USER_THEMES](state, obj) {
      state.newReport.themes = obj;
    },
  },

  actions: {
    getReports({ commit, dispatch }) {
      const project = helper.getItem('project');
      axios.get(`/api/reports?project=${project.id}&status=1`).then((response) => {
        commit(TYPES.SET_REPORTS, response.data);
      }).catch((error) => {
        dispatch('notifyOpen', { type: 0, message: 'Error, try again.' });
        throw new Error(error);
      });
    },

    getReportsByTheme({ dispatch, commit, state }, obj) {
      if (obj.isChecked) {
        axios.get(`/api/reports?theme=${obj.themeId}&status=1`).then((response) => {
          commit(TYPES.ADD_REPORTS_LIST, {
            data: response.data,
            theme: obj.themeId,
          });
        }).catch((error) => {
          dispatch('notifyOpen', { type: 0, message: 'Error, try again.' });
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

    getReport({ commit, dispatch }, obj) {
      axios.get(`/api/reports/${obj}`).then((response) => {
        commit(TYPES.SET_CURRENT_REPORT, response.data);
      }).then(() => {
        axios.get(`/api/report-medias/?report=${obj}`).then((response) => {
          commit(TYPES.SET_REPORT_MEDIAS, response.data[0]);
        });
      }).catch((error) => {
        dispatch('notifyOpen', { type: 0, message: 'Error, try again.' });
        throw new Error(error);
      });
    },

    getComments({ commit, dispatch }, obj) {
      axios.get(`/api/report-comments/?report=${obj}`).then((response) => {
        commit(TYPES.SET_REPORT_COMMENTS, response.data);
      }).catch((error) => {
        dispatch('notifyOpen', { type: 0, message: 'Error, try again.' });
        throw new Error(error);
      });
    },

    clearReports({ commit }) {
      commit(TYPES.CLEAR_REPORTS_LIST);
    },

    saveNewComment({ commit, dispatch }, obj) {
      const token = helper.getItem('token');
      const options = {};

      if (token) {
        options.headers = { authorization: `Token ${token}` };
      }

      return axios.post('/api/report-comments/', {
        text: obj.text,
        report: obj.report,
      }, options).then(() => {
        dispatch('notifyOpen', { type: 1, message: 'Comment Sent!' });
      }).catch((error) => {
        dispatch('notifyOpen', { type: 0, message: 'Error, try again.' });
        throw new Error(error);
      });
    },

    deleteComment({ commit, dispatch }, obj) {
      const token = helper.getItem('token');
      return axios.delete(`/api/report-comments/${obj}/`, {}, {
        headers: { authorization: `Token ${token}` },
      }).then(() => {
        commit(TYPES.REMOVE_COMMENT, obj);
        dispatch('notifyOpen', { type: 1, message: 'Comment Removed!' });
      }).catch((error) => {
        dispatch('notifyOpen', { type: 0, message: 'Error, try again.' });
        throw new Error(error);
      });
    },

    getUserThemes({ commit, dispatch }, obj) {
      axios.get(`/api/themes/?user=${obj}`).then((response) => {
        commit(TYPES.NEW_REPORT_USER_THEMES, response.data);
      }).catch((error) => {
        dispatch('notifyOpen', { type: 0, message: 'Error, try again.' });
        throw new Error(error);
      });
    },

    getProjectThemes({ commit, dispatch }) {
      const project = helper.getItem('project');
      axios.get(`/api/themes?project=${project.id}`).then((response) => {
        commit(TYPES.NEW_REPORT_USER_THEMES, response.data);
      }).catch((error) => {
        dispatch('notifyOpen', { type: 0, message: 'Error, try again.' });
        throw new Error(error);
      });
    },

    saveNewReport({ commit, dispatch }, obj) {
      const token = helper.getItem('token');
      return axios.post('/api/reports/', {
        name: obj.name,
        description: obj.description,
        theme: obj.theme,
        location: obj.location,
        tags: obj.tags,
      }, {
        headers: { authorization: `Token ${token}` },
      }).then((response) => {
        dispatch('notifyOpen', { type: 1, message: 'Report Sent!' });
        return response.data;
      }).catch((error) => {
        let messageError = '';
        const json = JSON.parse(error.response.request.responseText);

        if (json.location) {
          messageError = json.location[0];
        }

        if (json.detail) {
          messageError = json.detail;
        }

        dispatch('notifyOpen', { type: 0, message: messageError });
        throw new Error(error);
      });
    },

    uploadAndSaveFiles({ commit }, obj) {
      const token = helper.getItem('token');
      const data = new FormData();
      data.append('file', obj.file);
      data.append('title', 'test');
      data.append('description', 'bla bla bla');
      data.append('report_id', obj.id);

      const config = { headers: {
        'Content-Type': 'multipart/form-data',
        authorization: `Token ${token}`,
      } };
      return axios.post('/api/report-files/', data, config).then((response) => {
        console.log(response);
      }).catch((error) => {
        console.log(error);
      });
    },

    getGeoLocation({ commit }, obj) {
      const urlApi = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${obj.latitude},${obj.longitude}&key=${mapsKey}`;
      return axios.get(urlApi).then((response) => {
        if (response.data.results[0]) {
          return response.data.results[0].formatted_address;
        }
        return '';
      }).catch((error) => {
        throw new Error(error);
      });
    },
  },
};
