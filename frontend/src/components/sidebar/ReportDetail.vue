<template>
  <div>
    <navigation-bar
      :title="searchQuery && `${$t('message.sidebar.report.searchtitle')}: ${searchQuery}` || item.theme_name"
      :backButton="backButton"
      :closeButton="true"
      backTo="Theme"
      @openComponent="goBack" />

      <div class="map-box">
        <div class="box-flex scroll">
          <div class="header">
            <img :src="filePreview" v-if="filePreviewType == 'image'" alt="" v-cloak>
            <video v-if="filePreviewType == 'video'" width="622" height="200" autoplay controls v-cloak>
              <source :src="filePreview" type="video/mp4">
            </video>

            <div class="columns">
              <div class="column">
                <ul class="images">
                  <li v-for="(file, key) in files" :key="key" v-cloak>
                    <img v-if="file.media_type == 'image'" :src="file.thumbnail" @click.prevent="openFile(file)" alt="" v-cloak>
                    <img v-if="file.media_type == 'video'" src="~@/assets/img/video.png" @click.prevent="openFile(file)" alt="" v-cloak>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <div class="reports">
            <h1 :style="formatFontColor()" v-cloak>{{ item.name }}</h1>
            <small :style="formatFontColor()" v-cloak>{{ formatDate() }}</small><br/>
            <small :style="formatFontColor()" v-cloak>{{ $t('message.sidebar.report.by') }} {{ formatUsername() }}</small>
            <p v-html="formatDescription()" v-cloak></p>

            <div class="urls" v-if="item.urls" v-cloak>
              <strong>{{ $t('message.sidebar.report.links') }}</strong>
              <p v-for="(url, key) in item.urls" :key="key">
                <a :href="formatUrl(url)" target="_blank">{{ formatUrl(url) }}</a>
              </p>
            </div>

            <div class="tags">
              <small :style="formatColor()" :key="key" v-for="(tag, key) in item.tags">
                <a href="" @click.prevent="search(tag)">{{ tag }}</a>
              </small>
            </div>
          </div>

          <div class="columns is-mobile buttons">
            <div class="column">
              <a class="button share shared">
                <span class="icon-icon-share"></span> {{ $t('message.sidebar.report.share') }}
                <social-sharing
                  :url="formatURI()"
                  :title="item.name"
                  :description="item.description"
                  :quote="item.description"
                  :hashtags="formatTags()"
                  v-cloak
                  class="popover"
                  inline-template>
                  <div>
                    <div class="columns">
                      <div class="column">
                        <network network="facebook">
                          <i class="social-facebook"></i>
                        </network>
                      </div>
                      <div class="column">
                        <network network="twitter">
                          <i class="social-twitter"></i>
                        </network>
                      </div>
                    </div>
                  </div>
                </social-sharing>
              </a>
            </div>

            <div class="column">
              <a class="button share" @click.prevent="openComments" v-if="item.can_receive_comments">
                <span class="icon-icon-comment"></span> {{ $t('message.sidebar.report.comment') }} ({{ item.comments }})
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import bus from '@/helper/bus';
import helper from '@/helper';
import NavigationBar from './Navigation';

const socialSharing = require('vue-social-sharing');

export default {
  name: 'ReportDetail',

  components: { NavigationBar, socialSharing },

  data() {
    return {
      filePreview: '',
      filePreviewType: '',
      backButton: true,
    };
  },

  mounted() {
    bus.$on('clearFields', () => {
      this.filePreview = '';
      this.filePreviewType = '';
    });

    this.checkPreview();
  },

  computed: {
    ...mapGetters({
      item: 'getReport',
      files: 'getReportFiles',
      currentProject: 'getCurrentProject',
      searchQuery: 'searchQuery',
    }),
  },

  watch: {
    files() {
      this.checkPreview();
    },
  },

  methods: {
    ...mapActions([
      'getComments',
      'getTheme',
      'setSideBarConfigs',
      'searchReports',
      'getReport',
    ]),

    checkPreview() {
      if (this.files.length > 0) {
        this.filePreview = this.files[0].out;
        this.filePreviewType = this.files[0].media_type;
      } else {
        this.filePreview = '';
        this.filePreviewType = '';
      }
    },

    openFile(item) {
      this.filePreview = item.out;
      this.filePreviewType = item.media_type;
    },

    formatDate() {
      if (this.item.created_on) {
        return helper.formatDate(this.item.created_on);
      }
      return '';
    },

    formatColor() {
      return `background-color: #${this.item.theme_color} !important;`;
    },

    formatFontColor() {
      return `color: #${this.item.theme_color} !important;`;
    },

    formatDescription() {
      return (this.item.description ? this.item.description.replace(/(?:\r\n|\r|\n)/g, '<br />') : '');
    },

    formatUrl(url) {
      let tempUrl = url;
      if (!/^https?:\/\//i.test(tempUrl)) {
        tempUrl = `http://${tempUrl}`;
      }

      return tempUrl;
    },

    formatTags() {
      if (this.item.tags) {
        return this.item.tags.join(', ');
      }
      return '';
    },

    formatURI() {
      return `${window.location}/report/${this.item.id}`;
    },

    formatUsername() {
      if (this.item.created_by) {
        return this.item.created_by.username;
      }
      return '';
    },

    goBack() {
      if (this.searchQuery) {
        this.searchReports(this.searchQuery).then(() => {
          this.setSideBarConfigs({
            title: 'Results',
            tabActived: 'Search',
            backButton: false,
            isActived: true,
          });
        });
      } else {
        this.openTheme();
      }
    },

    openTheme() {
      this.getTheme(this.item.theme).then(() => {
        this.setSideBarConfigs({
          tabActived: 'Theme',
          isActived: true,
        }).then(() => {
          this.$router.push({ name: 'project', params: { path: this.currentProject.path } });
        });
      });
    },

    openComments() {
      this.getComments(this.item.id).then(() => {
        this.setSideBarConfigs({
          tabActived: 'Comments',
          isActived: true,
        });
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
.shared {
  .popover {
      background-color: #00cbff;
      border-radius: 5px;
      bottom: 55px;
      box-shadow: 0 0 5px #00cbff;
      color: #fff;
      left: 0px;
      padding-top: 7px;
      display: none;
      font-size: 40px;
      position: absolute;
      width: 267px;
      z-index: 4;
      text-align: center;

      &:before {
        border-top: 7px solid #00cbff;
        border-right: 7px solid transparent;
        border-left: 7px solid transparent;
        bottom: -7px;
        content: '';
        display: block;
        left: 50%;
        margin-left: -7px;
        position: absolute;
      }
    }

  &:hover {
    .popover {
      display: block;
      -webkit-animation: fade-in .5s linear 1, move-up .5s linear 1;
      -moz-animation: fade-in .5s linear 1, move-up .5s linear 1;
      -ms-animation: fade-in .5s linear 1, move-up .5s linear 1;
    }
  }
}

@-webkit-keyframes fade-in {
	from   { opacity: 0; }
	to { opacity: 1; }
}
@-moz-keyframes fade-in {
	from   { opacity: 0; }
	to { opacity: 1; }
}
@-ms-keyframes fade-in {
	from   { opacity: 0; }
	to { opacity: 1; }
}
@-webkit-keyframes move-up {
	from   { bottom: 55px; }
	to { bottom: 55px; }
}
@-moz-keyframes move-up {
	from   { bottom: 55px; }
	to { bottom: 55px; }
}
@-ms-keyframes move-up {
	from   { bottom: 55px; }
	to { bottom: 55px; }
}

.map-box {
  margin: auto;

  .box-flex {
    display: flex;
    flex-direction: column;
    height: 84vh;
  }

  .no-padding {
    padding-right: 0px !important;
  }

  .buttons {
    width: 100%;
    height: 64px;
    margin-left: 0px;
    position: absolute;
    bottom: 12px;

    .share {
      width: 100%;
      height: 50px;
      border-radius: 10px;
      background-color: #ffffff;
      box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.3);

      font-size: 17px;
      text-align: left;
      color: #000000;

      span {
        font-size: 20px;
        margin-right: 5px;
      }
    }
  }

  .header {
    width: 100%;
    text-align: center;

    img {
      max-height: 200px;
    }
  }

  ul.images {
    margin: 0 10px 0px 10px;
    white-space: nowrap;
    overflow-x: auto;
  }

  ul.images li {
    display: inline;
  }

  ul.images img {
    width: 86px;
    height: 86px;
    padding: 5px;
    cursor: pointer;
  }

  .scroll {
    overflow-y: auto;
    overflow-x: hidden;
    max-height: calc(100vh - 197px);
  }

  .reports {
    margin-left: 7px;
    margin-right: 7px;

    h1 {
      font-size: 20px;
      font-weight: bold;
      letter-spacing: -0.5px;
      text-align: left;
      color: #9012fe;
    }

    small {
      font-size: 12px;
      text-align: left;
      color: #9012fe;
    }

    p {
      font-size: 14px;
      color: #000000;
      margin-top: 25px;
    }
  }

  .urls {
    margin-top: 14px;

    p {
      margin-top: 0px;
    }
  }

  .tags {
    margin-top: 5px;

    small {
      margin-right: 3px;
      letter-spacing: -0.3px;
      text-align: center;
      padding: 5px;
      border-radius: 100px;
      background-color: #9012fe;

      a {
        font-size: 13px;
        color: #fff;
      }
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
