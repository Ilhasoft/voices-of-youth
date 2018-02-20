<template>
  <div>
    <header-index />
    <intro-project />
    <div class="columns is-marginless">
      <div class="column is-4 is-paddingless sidebar" v-show="sideBarActived">
        <side-bar />
      </div>

      <div class="column is-paddingless map-osm">
        <map-osm />
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import HeaderIndex from '@/components/header/Index';
import MapOsm from '@/components/shared/Map';
import SideBar from '@/components/sidebar/Index';
import IntroProject from '@/components/shared/IntroProject';

export default {
  name: 'Project',

  components: {
    HeaderIndex,
    SideBar,
    IntroProject,
    MapOsm,
  },

  computed: {
    ...mapGetters({
      sideBarActived: 'getSideBarIsActived',
    }),
  },
};
</script>

<style lang="scss" scoped>
.map-osm {
  z-index: 0;
  height: calc(100vh - 78px);
}

.sidebar {
  height: calc(100vh - 78px);
}
</style>
