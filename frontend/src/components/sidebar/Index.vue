<template>
  <div class="sidebar">
    <keep-alive>
      <component v-bind:is="tabActived" />
    </keep-alive>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import Themes from './Themes';
import Theme from './Theme';
import ReportDetail from './ReportDetail';
import Comments from './Comments';
import Search from './Search';

export default {
  name: 'Sidebar',

  components: { Themes, Theme, ReportDetail, Comments, Search },

  computed: {
    ...mapState({
      tabActived: state => state.SideBarStore.tabActived,
    }),
  },
};
</script>

<style lang="scss" scoped>
.sidebar {
  width: 622px;
  box-shadow: 0 9px 10px 0 rgba(0, 0, 0, 0.16);
  position: absolute;
  margin: auto;
  top: 78px;
  left: 0;
  bottom: 0;
  background-color: #fbfbfb;
  z-index: 10000;
}
</style>
