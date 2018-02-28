<template>
  <div>
    <navigation-bar
      :title="$t('message.sidebar.search.title')"
      :backButton="false"
      :closeButton="true" />
  
    <div class="map-box">
      <div class="columns">
        <div class="column scrolling">
          <div v-if="reports.length">
            <div class="columns is-mobile item" :key="key" v-for="(item, key) in reports">
              <div class="column is-3 m-auto center">
                <img v-if="item.last_image" :src="item.last_image.file" alt=""/>
              </div>

              <div class="column m-auto">
                <h1>{{ item.name }}</h1>
                <small>{{ item.created_by.first_name }}</small>

                <div class="tags">
                  <small :style="formatColor(item.theme_color)" :key="key" v-for="(tag, key) in item.tags">
                    <a href="" @click.prevent="search(tag)">{{ tag }}</a>
                  </small>
                </div>

                <p>{{ item.description }} <a href="" @click.prevent="openReport(item)" class="see-more">{{ $t('message.sidebar.search.more') }}</a></p>
              </div>
            </div>
          </div>
          <div v-else>
            <div class="columns">
              <div class="column no-result">
                <img :src="user.avatar" alt="">
                <p>{{ $t('message.sidebar.search.empty') }}</p>
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
import NavigationBar from './Navigation';

export default {
  name: 'Search',

  components: { NavigationBar },

  computed: {
    ...mapGetters({
      reports: 'getSearchReports',
      user: 'getUserData',
    }),
  },

  methods: {
    ...mapActions([
      'setSideBarConfigs',
      'getReport',
      'searchReports',
    ]),

    openReport(item) {
      this.setSideBarConfigs({
        tabActived: 'ReportDetail',
        isActived: true,
      }).then(() => {
        this.getReport(item.id);
      });
    },

    formatColor(color) {
      return `background-color: #${color} !important;`;
    },

    search(tag) {
      this.searchReports(tag).then(() => {
        this.setSideBarConfigs({
          title: 'Results',
          tabActived: 'Search',
          backButton: false,
          isActived: true,
        });
      });
    },
  },
};
</script>

<style lang="scss" scoped>
.map-box {
  margin: auto;
  padding-left: 25px;

  .tags {
    margin-top: 5px;

    small {
      margin-right: 3px;
      letter-spacing: -0.3px;
      text-align: center;
      padding: 5px;
      border-radius: 100px;

      a {
        font-size: 13px;
        color: #fff;
      }
    }
  }

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

  .see-more {
    color: #00cbff;
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
