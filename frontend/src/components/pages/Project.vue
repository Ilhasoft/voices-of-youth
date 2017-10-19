<template>
  <div>
    <header-index />
    <!-- PROJECT RIO -->
    <!-- <router-link to="/login"><h4>LOGIN</h4></router-link>
    <router-link to="/profile"><h4>PROFILE</h4></router-link>
    <router-link to="/my-reports"><h4>MY REPORTS</h4></router-link>
    <router-link to="/project/rio/gallery"><h4>GALLERY</h4></router-link>
    <router-link to="/project/rio/new-report"><h4>NEW REPORT</h4></router-link> -->
    <intro-project/>
    <side-bar v-show="sideBarActived" />
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

import HeaderIndex from '../header/Index';
import SideBar from '../sidebar/Index';
import IntroProject from '../shared/IntroProject';

export default {
  name: 'Project',

  components: { HeaderIndex, SideBar, IntroProject },

  computed: {
    ...mapGetters({
      sideBarActived: 'getSideBarIsActived',
    }),
  },
};
</script>
