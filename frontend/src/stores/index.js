import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

import HeaderStore from './header';
import UserStore from './user';
import ProjectStore from './project';
import SideBarStore from './sidebar';
import ThemeStore from './theme';
import ReportStore from './report';
import GalleryStore from './gallery';
import NotifyStore from './notify';
import SearchStore from './search';
import HomeStore from './home';

Vue.use(Vuex);

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
    SearchStore,
    HomeStore,
  },
});
