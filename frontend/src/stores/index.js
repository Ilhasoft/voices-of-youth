import Vue from 'vue';
import Vuex from 'vuex';

import HeaderStore from './header';
import UserStore from './user';
import ProjectStore from './project';
import SideBarStore from './sidebar';
import ThemeStore from './theme';
import ReportStore from './report';
import GalleryStore from './gallery';
import NotifyStore from './notify';

Vue.use(Vuex);

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
