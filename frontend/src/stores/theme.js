import axios from 'axios';
import * as TYPES from './types';
import helper from '../helper';

export default {
  state: {
    all: [],
    dateFrom: '',
    dateTo: '',
  },

  getters: {
    getThemes: state => state.all,
  },

  /* eslint-disable no-param-reassign */
  mutations: {
    [TYPES.SET_THEMES](state, obj) {
      state.all = obj;
    },
  },

  actions: {
    getThemes({ commit }) {
      const project = helper.getItem('project');
      axios.get(`/api/themes?project=${project.id}`).then((response) => {
        commit(TYPES.SET_THEMES, response.data);
      }).catch((error) => {
        throw new Error(error);
      });
    },
  },
};
