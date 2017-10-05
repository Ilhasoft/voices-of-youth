import Vue from 'vue';
import Vuex from 'vuex';

import HeaderStore from './header';
import UserStore from './user';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    HeaderStore,
    UserStore,
  },
});
