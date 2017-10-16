<template>
  <div class="sidebar">
    <div class="columns header is-mobile">
      <div class="column is-1 m-auto">
        <svg v-show="buttonBack" xmlns="http://www.w3.org/2000/svg" width="26" height="24" viewBox="0 0 26 24" class="back">
            <g fill="none" fill-rule="evenodd" stroke="#9B9FA3" stroke-linecap="round" stroke-linejoin="round" stroke-width="4">
              <path d="M23.141 11.719H3.725M12.513 21.424l-9.705-9.705 9.705-9.706"/>
            </g>
        </svg>
      </div>

      <div class="column has-text-center m-auto header-title">
        {{ headerTitle }}
      </div>

      <div class="column is-1 m-auto">
        <svg v-show="buttonClose" xmlns="http://www.w3.org/2000/svg" width="23" height="23" viewBox="0 0 23 23">
          <g fill="none" fill-rule="evenodd" stroke="#9B9FA3" stroke-linecap="round" stroke-linejoin="round" stroke-width="4">
            <path d="M20.475 2.46L2.49 20.444M2.49 2.46l17.985 17.985"/>
          </g>
        </svg>
      </div>
    </div>

    <!-- <comments /> -->
    <!-- <thematic-maps /> -->
    <!-- <theme /> -->
    <!-- <report-detail /> -->
    <search />
  </div>
</template>

<script>
import ThematicMaps from './ThematicMaps';
import Theme from './Theme';
import ReportDetail from './ReportDetail';
import Comments from './Comments';
import Search from './Search';

export default {
  name: 'Sidebar',

  components: { ThematicMaps, Theme, ReportDetail, Comments, Search },

  data() {
    return {
      buttonBack: true,
      buttonClose: true,
      headerTitle: 'Thematic Map',
    };
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
  // background-color: red;
  z-index: 10000;

  .header {
    height: 62px;
    background: #fff;
    // margin: 0px 0px 15px 0px;
    margin: 0px 0px -5px 0px;
  }

  .back {
    margin-left: 23px;
  }

  .has-text-center {
    text-align: center;
  }

  .m-auto {
    margin: auto;
  }

  .p-top {
    padding-top: 0px;
  }

  .header-title {
    font-size: 16px;
    letter-spacing: -0.4px;
    color: #9b9fa3;
  }
}
</style>
