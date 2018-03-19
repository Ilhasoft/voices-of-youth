<template>
  <div>
    <navigation-bar
      :title="item.name"
      :backButton="true"
      :closeButton="true"
      backTo="Themes"
      @openComponent="openThemes" />

    <div class="map-box">
      <div class="columns is-marginless">
        <div class="column is-paddingless">
          <div class="columns is-mobile is-marginless header" :style="formatColor(item.color)" v-cloak>
            <div class="column is-2 pin">
              <svg xmlns="http://www.w3.org/2000/svg" width="25" height="31" viewBox="0 0 25 31">
                  <g fill="none" fill-rule="evenodd" stroke="#FFF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" transform="translate(1.283 1.868)">
                    <path d="M22.371 11.194c0 8.707-11.185 16.17-11.185 16.17S0 19.901 0 11.194C0 5.012 5.008 0 11.186 0 17.363 0 22.37 5.012 22.37 11.194z"/>
                    <ellipse cx="11.186" cy="11.194" rx="3.729" ry="3.731"/>
                  </g>
              </svg>
            </div>

            <div class="column m-auto">
              <h1 v-cloak>{{ item.name }}</h1>
            </div>
          </div>

          <div class="scroll">
            <div class="columns">
              <div class="column text">
                <small :style="formatFontColor()" v-cloak>{{ formatDate(item.created_on) }}</small>
                <p v-cloak>{{ item.description }}</p>
              </div>
            </div>

            <div class="columns">
              <div class="column tags">
                <small :style="formatColor()" :key="key" v-for="(tag, key) in item.tags" v-cloak>
                  <a href="" @click.prevent="search(tag)">{{ tag }}</a>
                </small>
              </div>
            </div>

            <div class="columns reports">
              <div class="column">
                <h1 :style="formatFontColor()" v-cloak>{{ item.reports_count }} {{ $t('message.sidebar.theme.reports') }}</h1>
              </div>
            </div>

            <div class="columns medias">
              <div class="column">
                <ul>
                  <li :key="key" v-for="(report, key) in lastReports" v-cloak>
                    <img :src="report.thumbnail" @click.prevent="openReport(report)" alt="" v-cloak>
                  </li>
                </ul>
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
  name: 'Theme',

  components: { NavigationBar },

  computed: {
    ...mapGetters({
      item: 'getTheme',
      lastReports: 'getLastReports',
      currentProject: 'getCurrentProject',
    }),
  },

  methods: {
    ...mapActions([
      'setSideBarConfigs',
      'getReport',
      'searchReports',
    ]),

    formatDate() {
      if (this.item.created_on) {
        const date = new Date(this.item.created_on);
        return `${date.toLocaleString('en-use', { month: 'short' })} ${date.getDay()}, ${date.getFullYear()}`;
      }
      return '';
    },

    formatColor() {
      return `background-color: #${this.item.color} !important;`;
    },

    formatFontColor() {
      return `color: #${this.item.color} !important;`;
    },

    openThemes() {
      this.setSideBarConfigs({
        tabActived: 'Themes',
        isActived: true,
      });
    },

    openReport(item) {
      this.setSideBarConfigs({
        tabActived: 'ReportDetail',
        isActived: true,
      }).then(() => {
        this.getReport(item.id);
      });
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

  .m-left {
    margin-left: 15px;
  }

  .scroll {
    overflow-y: auto;
    overflow-x: hidden;
    max-height: calc(100vh - 266px);
    position: relative;
  }

  .header {
    width: 100%;
    height: 131px;
  }

  .pin {
    padding-left: 30px;
    margin: auto;
  }

  .m-auto {
    margin: auto;
  }

  .center {
    text-align: center;
  }

  .medias {
    margin: 15px 0px 0px 7px;

    li {
      display: inline;
    }

    li:nth-child(5):after {
      content: "\A";
      white-space: pre;
    }

    img {
      width: 100px;
      height: 100px;
      margin: 0px 5px 5px 5px;
      cursor: pointer;
    }
  }

  .reports {
    margin: 15px 0px 0px 7px;

    h1 {
      font-size: 20px;
      font-weight: bold;
      letter-spacing: -0.5px;
      text-align: left;
    }
  }

  .tags {
    margin-left: 18px;
    margin-right: 35px;
    display: inline-flex;
    
    small {
      margin-bottom: 5px;
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

  .text {
    margin-left: 18px;
    margin-right: 35px;
    text-align: justify;

    small {
      font-size: 18px;
      font-weight: bold;
      letter-spacing: -0.4px;
      text-align: left;
      color: #9012fe;
    }

    p {
      font-size: 15px;
      line-height: 1.33;
      letter-spacing: -0.4px;
      color: #000000;
      margin-top: 30px;
    }
  }

  h1 {
    font-size: 25px;
    font-weight: bold;
    letter-spacing: -0.6px;
    text-align: left;
    color: #ffffff;
  }
}
</style>
