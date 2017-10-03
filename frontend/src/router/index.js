import Vue from 'vue';
import Router from 'vue-router';
import Home from '../components/pages/Home';
import Project from '../components/pages/Project';

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
    },

    // project selected
    {
      path: '/project/:id',
      name: 'Project',
      component: Project,
    },
  ],
});
