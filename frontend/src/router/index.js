import Vue from 'vue';
import Router from 'vue-router';

import HomePage from '../components/pages/Home';
import ProjectPage from '../components/pages/Project';
import LoginPage from '../components/pages/Login';
import ProfilePage from '../components/pages/Profile';
import MyReportsPage from '../components/pages/MyReports';
import GalleryPage from '../components/pages/Gallery';
import NewReportPage from '../components/pages/NewReport';

import stores from '../stores';

Vue.use(Router);

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
        stores.dispatch('setProjects');
        stores.dispatch('setCurrentProject');
        stores.dispatch('setCurrentUser');

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
        stores.dispatch('setProjects');
        stores.dispatch('setCurrentProject');
        stores.dispatch('setCurrentUser');

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
      path: '/login',
      name: 'login',
      component: LoginPage,
      beforeEnter: (to, from, next) => {
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
      name: 'Profile',
      component: ProfilePage,
      beforeEnter: (to, from, next) => {
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
      name: 'MyReports',
      component: MyReportsPage,
      beforeEnter: (to, from, next) => {
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

    {
      path: '/project/:id/new-report',
      name: 'NewReport',
      component: NewReportPage,
      beforeEnter: (to, from, next) => {
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
  ],
});
