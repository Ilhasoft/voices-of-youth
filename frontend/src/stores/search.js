import * as TYPES from './types';

export default {
  state: {
    query: '',
  },

  getters: {
    searchQuery: state => state.query,
  },

  /* eslint-disable no-param-reassign */
  mutations: {
    [TYPES.SET_SEARCH_QUERY](state, query) {
      state.query = query;
    },
  },
  /* eslint-enable no-param-reassign */

  actions: {
    setSearchQuery: ({ commit }, query) => {
      commit(TYPES.SET_SEARCH_QUERY, query);
    },
  },
};
