import axios from 'axios';

export default {
//   state: {
//     all: [],
//     current: {},
//     language: '',
//     disclaimer: true,
//   },

//   getters: {
//     getAllProjects: state => state.all,
//     getCurrentProject: state => state.current,
//     getDisclaimerProject: state => state.disclaimer,
//     getProjectLanguages: state => state.current.languages,
//     getCurrentLanguage: state => state.language,
//   },

  /* eslint-disable no-param-reassign */
//   mutations: {
//     [TYPES.SET_PROJECTS_LIST](state, obj) {
//       state.all = obj;
//     },

//     [TYPES.SET_CURRENT_PROJECT](state, obj) {
//       if (obj) {
//         state.current = obj;
//         document.title = `Voices of Youth - ${obj.name}`;
//       }
//     },

//     [TYPES.SET_DISCLAIMER_PROJECT](state, obj) {
//       state.disclaimer = obj;
//     },

//     [TYPES.SET_CURRENT_LANGUAGE](state, obj) {
//       state.language = obj;
//     },
//   },

  actions: {
    getHomeSlide: async () => {
      const data = await axios.get('/api/home-slide');
      return data;
    },

    getAboutProject: async () => {
      const data = await axios.get('/api/home-about');
      return data[0];
    },

    getProjects: async ({ commit }, obj) => {
      let queryString = '';

      if (obj && obj.page) {
        queryString = `?page=${obj.page}&page_size=${obj.pageSize}${(obj.order ? '&order=1' : '')}`;
      }

      const data = await axios.get(`/api/projects/${queryString}`);
      return data;
    },
  },
};
