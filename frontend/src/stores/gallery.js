import axios from 'axios';
import * as TYPES from './types';
import helper from '../helper';

export default {
  state: {
    all: [],
    total: 0,
    page: 0,
    next: '',
    previous: '',
  },

  getters: {
    galleryImages(state) {
      if (state.all) {
        return state.all.reduce((items, it, i) => {
          const ix = Math.floor(i / 5);
          const newArray = items;

          if (!newArray[ix]) {
            newArray[ix] = [];
          }

          newArray[ix].push(it);
          return newArray;
        }, []);
      }
      return state.all;
    },

    galleryTotal: state => state.total,
    galleryPagination: state => Math.ceil(state.total / 20),
    galleryNextUrl: state => state.next,
    galleryPreviousUrl: state => state.previous,
    galleryCurrentPage: state => state.page,
  },

  /* eslint-disable no-param-reassign */
  mutations: {
    [TYPES.SET_GALLERY_IMAGES](state, obj) {
      state.all = obj.results;
      state.total = obj.count;
      state.next = (obj.next ? obj.next : '');
      state.previous = (obj.previous ? obj.previous : '');
    },

    [TYPES.SET_GALLERY_PAGE](state, obj) {
      state.page = obj;
    },
  },

  actions: {
    getGalleryImages: async ({ commit, dispatch }, obj) => {
      let queryString = '';
      let currentPage = 1;

      if (obj && obj.page) {
        queryString = `&page=${obj.page}`;
        currentPage = obj.page;
      }

      const project = helper.getItem('project');
      const data = await axios.get(`/api/report-files/?project=${project.id}${queryString}&page_size=20&media_type=image`);
      commit(TYPES.SET_GALLERY_IMAGES, data);
      commit(TYPES.SET_GALLERY_PAGE, currentPage);
    },
  },
};
