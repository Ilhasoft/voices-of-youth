<template>
  <div>
    <header-index />
    <intro-project />
    <div class="columns is-marginless">
      <div class="column is-4 is-paddingless" v-show="sideBarActived">
        <side-bar />
      </div>

      <div class="column is-paddingless map-osm">
        <map-osm />
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import HeaderIndex from '../header/Index';
import MapOsm from '../shared/Map';
import SideBar from '../sidebar/Index';
import IntroProject from '../shared/IntroProject';

export default {
  name: 'Project',

  components: {
    HeaderIndex,
    SideBar,
    IntroProject,
    MapOsm,
  },

  mounted() {
    this.getReports();
  },

  computed: {
    ...mapGetters({
      sideBarActived: 'getSideBarIsActived',
    }),
  },

  methods: {
    ...mapActions([
      'getReports',
    ]),
  },
};
</script>

<style lang="scss" scoped>
.map-osm {
  z-index: 0;
  height: 91vh;
}
</style>
