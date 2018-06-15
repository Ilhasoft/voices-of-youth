import axios from 'axios';

export default {
  actions: {
    getHomeSlide: async () => {
      const data = await axios.get('/api/home-slide/');
      return data;
    },

    getAboutProject: async () => {
      const data = await axios.get('/api/home-about/');
      return data[0];
    },

    getHomeProjects: async ({ commit }, obj) => {
      let queryString = '';

      if (obj && obj.page) {
        queryString = `?page=${obj.page}&page_size=${obj.pageSize}${(obj.order ? '&order=1' : '')}`;
      }

      const data = await axios.get(`/api/projects/${queryString}`, {
        headers: {
          Authorization: '',
        },
      });
      return data;
    },

    getHomeReports: async ({ commit }, obj) => {
      let queryString = '';

      if (obj && obj.page) {
        queryString = `&page=${obj.page}&page_size=${obj.pageSize}`;
      }

      const data = await axios.get(`/api/reports/?featured=1${queryString}`);
      return data;
    },

    submitFormContact: async ({ commit }, obj) => {
      const promise = new Promise(async (resolve, reject) => {
        try {
          const data = await axios.post('/api/home-contact/', obj);
          resolve(data);
        } catch (error) {
          reject(error.response.data);
        }
      });
      return promise;
    },
  },
};
