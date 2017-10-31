<template>
  <div class="map-box">
    <div class="columns">
      <div class="column no-padding">
        <div class="columns header">
          <div class="column no-padding">
            <img :src="filePreview" v-if="filePreviewType == 'image'" alt="">
            <video v-if="filePreviewType == 'video'" width="622" height="200" autoplay controls>
              <source :src="filePreview" type="video/mp4">
            </video>
          </div>
        </div>

        <div class="columns">
          <div class="column">
            <ul class="images">
              <li v-for="(file, key) in files" :key="key">
                <img v-if="file.media_type == 'image'" :src="file.file" @click.prevent="openFile(file)" alt="">
                <img v-if="file.media_type == 'video'" src="../../assets/img/report-example.png" @click.prevent="openFile(file)" alt="">
              </li>
            </ul>
          </div>
        </div>

        <div class="columns reports">
          <div class="column">
            <h1 :style="formatFontColor()">{{ item.name }}</h1>
            <small :style="formatFontColor()">{{ formatDate() }}</small>
            <p>{{ item.description }}</p>
          </div>
        </div>

        <div class="columns">
          <div class="column tags">
            <small :style="formatColor()" :key="key" v-for="(tag, key) in item.tags">{{ tag }}</small>
          </div>
        </div>

        <div class="columns buttons">
          <div class="column">
            <a class="button share">
              <span class="icon-icon-share"></span> Share
            </a>
          </div>

          <div class="column">
            <a class="button share" @click.prevent="openComments" v-if="item.can_receive_comments">
              <span class="icon-icon-comment"></span> Comment
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import bus from '../../helper/bus';

export default {
  name: 'ReportDetail',

  data() {
    return {
      filePreview: '',
      filePreviewType: '',
    };
  },

  mounted() {
    bus.$on('clearFields', () => {
      this.filePreview = '';
      this.filePreviewType = '';
    });
  },

  computed: {
    ...mapGetters({
      item: 'getReport',
      files: 'getReportFiles',
    }),
  },

  methods: {
    ...mapActions([
      'getComments',
      'setSideBarConfigs',
    ]),

    openFile(item) {
      this.filePreview = item.file;
      this.filePreviewType = item.media_type;
    },

    formatDate() {
      const date = new Date(this.item.created_on);
      return `${date.toLocaleString('en-use', { month: 'short' })} ${date.getDay()}, ${date.getFullYear()}`;
    },

    formatColor() {
      return `background-color: #${this.item.theme_color} !important;`;
    },

    formatFontColor() {
      return `color: #${this.item.theme_color} !important;`;
    },

    openComments() {
      this.getComments(this.item.id).then(() => {
        this.setSideBarConfigs({
          title: 'Comments',
          tabActived: 'Comments',
          backButton: true,
          backTo: 'ReportDetail',
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

  .no-padding {
    padding-right: 0px !important;
  }

  .buttons {
    margin-left: 7px;

    .share {
      width: 267.8px;
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
    
    img {
      width: 100%;
      height: 200px;
    }
  }

  ul.images {
    width: 622px;
    margin: 0;
    padding: 0;
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
      margin-top: 30px;
    }
  }

  .tags {
    margin-left: 18px;
    margin-right: 35px;

    small {
      margin-right: 3px;
      font-size: 13px;
      letter-spacing: -0.3px;
      text-align: center;
      color: #fff;
      padding: 5px;
      border-radius: 100px;
      background-color: #9012fe;
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
