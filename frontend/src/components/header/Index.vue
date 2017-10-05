<template>
  <section>
    <div class="columns">
      <div class="column is-3">
        <projects-menu v-show="showProjects" />
        <back-menu v-show="showBackButton" />
      </div>
  
      <div class="column">
        <div class="header menu">
          <header-menu />
        </div>
      </div>

      <div class="column is-3">
        <div class="header account" v-show="userIsLogged">
          <right-menu />
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { mapGetters } from 'vuex';

import ProjectsMenu from './Projects';
import BackMenu from './Back';
import HeaderMenu from './Menu';
import RightMenu from './RightSide';

export default {
  name: 'Header',

  components: { ProjectsMenu, BackMenu, HeaderMenu, RightMenu },

  computed: {
    ...mapGetters({
      userIsLogged: 'userIsLogged',
      showProjects: 'menuProjectsVisibled',
      showBackButton: 'menuBackVisibled',
    }),
  },
};
</script>

<style lang="scss" scoped>
section {
  border-bottom: 12px solid #00cbff;
}

.header.menu {
  height: 66px;
  padding-top: 22px;
}

.header.account {
  color: rgba(0, 0, 0, 0.7);
  height: 66px;
  padding: 1.25rem 0;
}

.header {
  vertical-align: middle;
  position: relative;
  text-align: center;
}
</style>
