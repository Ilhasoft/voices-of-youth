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

import stores from '@/stores';
import helper from '@/helper';

Vue.use(Router);

const dispatchStores = () => {
  stores.dispatch('setProjects');
  stores.dispatch('setCurrentProject');
  stores.dispatch('setCurrentUser');

  const token = helper.getItem('token');

  if (token) {
    const authorization = 'Authorization';
    axios.defaults.headers.common[authorization] = `Token ${token}`;
  }
};

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomePage,
    },

    // project selected
    // TODO: Refactor routes
    {
      path: '/project/:path',
      name: 'project',
      component: ProjectPage,
      beforeEnter: (to, from, next) => {
        dispatchStores();
        stores.dispatch('updateHeaderConfig', {
          showMenu: true,
          showProjects: true,
          showBackButton: false,
        }).then(() => {
          next();
        });
      },
    },

    {
      path: '/project/:path/gallery',
      name: 'gallery',
      component: GalleryPage,
      beforeEnter: (to, from, next) => {
        dispatchStores();
        stores.dispatch('updateHeaderConfig', {
          menuTitle: 'Gallery',
          showMenu: false,
          showProjects: false,
          showBackButton: true,
        }).then(() => {
          next();
        });
      },
    },

    {
      path: '/project/:path/new-report',
      name: 'newreport',
      component: NewReportPage,
      beforeEnter: (to, from, next) => {
        dispatchStores();
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
      path: '/login',
      name: 'login',
      component: LoginPage,
      beforeEnter: (to, from, next) => {
        dispatchStores();
        stores.dispatch('updateHeaderConfig', {
          menuTitle: 'Login',
          showMenu: false,
          showProjects: false,
          showBackButton: true,
        }).then(() => {
          next();
        });
      },
    },

    {
      path: '/profile',
      name: 'profile',
      component: ProfilePage,
      beforeEnter: (to, from, next) => {
        dispatchStores();
        stores.dispatch('updateHeaderConfig', {
          menuTitle: 'My Profile',
          showMenu: false,
          showProjects: false,
          showBackButton: true,
        }).then(() => {
          next();
        });
      },
    },

    {
      path: '/my-reports',
      name: 'my-reports',
      component: MyReportsPage,
      beforeEnter: (to, from, next) => {
        dispatchStores();
        stores.dispatch('updateHeaderConfig', {
          menuTitle: 'My Reports',
          showMenu: false,
          showProjects: false,
          showBackButton: true,
        }).then(() => {
          next();
        });
      },
    },
  ],
});
