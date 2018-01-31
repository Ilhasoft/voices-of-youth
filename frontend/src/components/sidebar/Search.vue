<template>
  <div>
    <navigation-bar
      title="Results"
      :backButton="false"
      :closeButton="true" />
  
    <div class="map-box">
      <div class="columns">
        <div class="column scrolling">
          <div v-if="searchReports.length">
            <div class="columns is-mobile item" :key="key" v-for="(item, key) in searchReports">
              <div class="column is-3 m-auto center">
                <img v-if="item.last_image" :src="item.last_image.file" alt=""/>
              </div>

              <div class="column m-auto">
                <h1>{{ item.name }}</h1>
                <small>{{ item.created_by.first_name }}</small>
                <p>{{ item.description }} <a href="" @click.prevent="openReport(item)" class="see-more">See more</a></p>
              </div>
            </div>
          </div>
          <div v-else>
            <div class="columns">
              <div class="column no-result">
                <img src="~@/assets/img/my-report-rejected.png" alt="">
                <p>No results found</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import bus from '@/helper/bus';
import NavigationBar from './Navigation';

export default {
  name: 'Search',

  components: { NavigationBar },

  computed: {
    ...mapGetters({
      searchReports: 'getSearchReports',
    }),
  },

  methods: {
    ...mapActions([
      'setSideBarConfigs',
    ]),

    openReport(item) {
      this.setSideBarConfigs({
        tabActived: 'ReportDetail',
        isActived: true,
      }).then(() => {
        bus.$emit('openReport', item);
      });
    },
  },
};
</script>

<style lang="scss" scoped>
.map-box {
  margin: auto;
  padding-left: 25px;

  .no-result {
    text-align: center;
    margin-top: 70px;

    img {
      width: 64px !important;
      height: 64px  !important;
    }

    p {
      text-align: center;
      font-size: 20px;
      color: #000000;
    }
  }

  .scrolling {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    overflow-y: auto;
    margin-top: 62px;
    margin-left: 20px;
    width: 96%;

    .item {
      margin-top: 15px;
      margin-bottom: 15px;
      width: 100%;
      min-height: 125px;
      border-radius: 10px;
      background-color: #fff;
      box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.16);

      h1 {
        font-size: 16px;
        font-weight: 500;
        color: #000000;
      }

      p {
        font-size: 15px;
        line-height: 1.33;
        letter-spacing: -0.4px;
        text-align: left;
        color: #000000;
      }
      
      small {
        font-size: 12px;
        font-weight: 500;
        text-align: left;
      }

      img {
        width: 89px;
        height: 89px;
      }

      .m-auto {
        margin: auto;
      }

      .center {
        text-align: center;
      }
    }
  }
}
</style>
