import Vue from 'vue';
import Router from 'vue-router';
import axios from 'axios';

import HomePage from '@/components/pages/Home';
import ProjectPage from '@/components/pages/Project';
import LoginPage from '@/components/pages/Login';
import ProfilePage from '@/components/pages/Profile';
import MyReportsPage from '@/components/pages/MyReports';
import GalleryPage from '@/components/pages/Gallery';
import NewReportPage from '@/components/pages/NewReport';
import EditReportPage from '@/components/pages/EditReport';
import ProjectsPage from '@/components/pages/Projects';
import ReportsPage from '@/components/pages/Reports';

import stores from '@/stores';
import helper from '@/helper';
import i18n from '@/translate';

Vue.use(Router);

if (process.env.BACKEND_SERVER) {
  axios.defaults.baseURL = process.env.BACKEND_SERVER;
}

axios.interceptors.request.use((config) => {
  if (config.url[config.url.length-1] !== '/') {
    config.url += '/';
  }
  return config;
});

async function dispatchStores(path) {
  const token = helper.getItem('token');

  if (token) {
    const authorization = 'Authorization';
    axios.defaults.headers.common[authorization] = `Token ${token}`;
  }

  await stores.dispatch('setUserProjects');
  await stores.dispatch('setCurrentProject', path);
  await stores.dispatch('setCurrentUser');

  return Promise.resolve();
}

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage,
      beforeEnter: async (to, from, next) => {
        await dispatchStores({ path: to.params.path });
        next();
      },
    },

    {
      path: '/projects',
      name: 'projects',
      component: ProjectsPage,
      beforeEnter: async (to, from, next) => {
        await dispatchStores({ path: to.params.path });
        next();
      },
    },

    {
      path: '/reports',
      name: 'reports',
      component: ReportsPage,
      beforeEnter: async (to, from, next) => {
        await dispatchStores({ path: to.params.path });
        next();
      },
    },

    {
      path: '/project/:path',
      name: 'project',
      component: ProjectPage,
      beforeEnter: async (to, from, next) => {
        await dispatchStores({ path: to.params.path });
        await stores.dispatch('updateHeaderConfig', {
          showMenu: true,
          showProjects: true,
          showBackButton: false,
        });
        await stores.dispatch('getReports');
        next();
      },
    },

    {
      path: '/project/:path/gallery',
      name: 'gallery',
      component: GalleryPage,
      beforeEnter: async (to, from, next) => {
        await dispatchStores({ path: to.params.path });
        await stores.dispatch('showDisclaimerProject', false);
        await stores.dispatch('updateHeaderConfig', {
          menuTitle: i18n.t('message.navigator.gallery'),
          showMenu: false,
          showProjects: false,
          showBackButton: true,
        });
        next();
      },
    },

    {
      path: '/project/:path/new-report',
      name: 'newreport',
      component: NewReportPage,
      beforeEnter: async (to, from, next) => {
        await dispatchStores({ path: to.params.path });
        await stores.dispatch('showDisclaimerProject', false);
        await stores.dispatch('updateHeaderConfig', {
          menuTitle: '',
          showMenu: true,
          showProjects: true,
          showBackButton: false,
        });
        next();
      },
    },

    {
      path: '/project/:path/edit-report/:id',
      name: 'editreport',
      component: EditReportPage,
      props: true,
      beforeEnter: async (to, from, next) => {
        await dispatchStores({ path: to.params.path });
        await stores.dispatch('showDisclaimerProject', false);
        stores.dispatch('updateHeaderConfig', {
          menuTitle: '',
          showMenu: true,
          showProjects: true,
          showBackButton: false,
        }).then(() => {
          next();
        });
      },
    },

    {
      path: '/project/:path/report/:id',
      name: 'report',
      component: ProjectPage,
      props: true,
      beforeEnter: async (to, from, next) => {
        await dispatchStores({ path: to.params.path });
        await stores.dispatch('showDisclaimerProject', false);
        await stores.dispatch('setSideBarConfigs', {
          tabActived: 'ReportDetail',
          isActived: true,
        });
        await stores.dispatch('updateHeaderConfig', {
          menuTitle: '',
          showMenu: true,
          showProjects: true,
          showBackButton: false,
        });
        await stores.dispatch('getReports');
        await stores.dispatch('getReport', to.params.id);
        next();
      },
    },

    {
      path: '/project/:path/login',
      name: 'login',
      component: LoginPage,
      beforeEnter: async (to, from, next) => {
        await dispatchStores({ path: to.params.path });
        await stores.dispatch('showDisclaimerProject', false);
        await stores.dispatch('updateHeaderConfig', {
          menuTitle: i18n.t('message.navigator.login'),
          showMenu: false,
          showProjects: false,
          showBackButton: true,
        });
        next();
      },
    },

    {
      path: '/project/:path/profile',
      name: 'profile',
      component: ProfilePage,
      beforeEnter: async (to, from, next) => {
        await dispatchStores({ path: to.params.path });
        await stores.dispatch('showDisclaimerProject', false);
        await stores.dispatch('updateHeaderConfig', {
          menuTitle: i18n.t('message.navigator.myprofile'),
          showMenu: false,
          showProjects: false,
          showBackButton: true,
        });
        next();
      },
    },

    {
      path: '/project/:path/my-reports',
      name: 'my-reports',
      component: MyReportsPage,
      beforeEnter: async (to, from, next) => {
        await dispatchStores({ path: to.params.path });
        await stores.dispatch('showDisclaimerProject', false);
        await stores.dispatch('updateHeaderConfig', {
          menuTitle: i18n.t('message.navigator.myreports'),
          showMenu: false,
          showProjects: false,
          showBackButton: true,
        });
        next();
      },
    },
  ],
});
