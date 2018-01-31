import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

import helper from '@/helper';

import HeaderStore from './header';
import UserStore from './user';
import ProjectStore from './project';
import SideBarStore from './sidebar';
import ThemeStore from './theme';
import ReportStore from './report';
import GalleryStore from './gallery';
import NotifyStore from './notify';

Vue.use(Vuex);

const token = helper.getItem('token');

if (token) {
  const authorization = 'Authorization';
  axios.defaults.headers.common[authorization] = `Token ${token}`;
}

axios.interceptors.response.use(
  ({ data }) => data,
  error => Promise.reject(error),
);

export default new Vuex.Store({
  modules: {
    HeaderStore,
    UserStore,
    ProjectStore,
    SideBarStore,
    ThemeStore,
    ReportStore,
    GalleryStore,
    NotifyStore,
  },
});
