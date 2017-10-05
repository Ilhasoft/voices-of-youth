import Vue from 'vue';
import Router from 'vue-router';
import HomePage from '../components/pages/Home';
import ProjectPage from '../components/pages/Project';
import LoginPage from '../components/pages/Login';
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
    {
      path: '/project/:id',
      name: 'Project',
      component: ProjectPage,
      beforeEnter: (to, from, next) => {
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
      path: '/login',
      name: 'Login',
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
  ],
});
