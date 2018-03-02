<template>
  <div 
    class="column is-2 notification-box" 
    @mouseover.prevent="isVisible = true" 
    @mouseout="isVisible = false"
    v-if="userIsLogged && userIsMapper">
    
    <div class="label" v-if="notifications.length"></div>
    <img class="img" src="~@/assets/img/header-bell.png">
    
    <div 
      class="notification-item" 
      @mouseover.prevent="isVisible = true" 
      @mouseout="isVisible = false" 
      :class="[isVisible ? 'fade-in' : 'fade-out']">
      <h4>{{ $t('message.header.notifications.title') }}</h4>
      
      <div class="item" v-if="notifications.length" :key="key" v-for="(item, key) in notifications">
        <a href="" @click.prevent="cleanNotification(item)">
          <div class="item-left" v-if="item.report.last_image">
            <div class="thumbnail">
              <img :src="item.report.last_image.file" alt="">
            </div>
          </div>

          <div class="item-right">
            <p v-html="formatMessage(item)"></p>
            <small>{{ formatDate(item.modified_on) }}</small>
          </div>
        </a>
      </div>
      <div v-if="notifications.length === 0">
        {{ $t('message.header.notifications.empty') }}
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import helper from '@/helper';
import router from '@/router/';

export default {
  name: 'Notification',

  data() {
    return {
      isVisible: false,
    };
  },

  mounted() {
    if (this.userIsLogged && this.userIsMapper) {
      this.getNotifications();
    }
  },

  computed: {
    ...mapGetters({
      userIsLogged: 'userIsLogged',
      userIsMapper: 'userIsMapper',
      notifications: 'getNotifications',
      currentProject: 'getCurrentProject',
    }),
  },

  methods: {
    ...mapActions([
      'getNotifications',
      'setSideBarConfigs',
      'setNotificationRead',
      'getReport',
    ]),

    formatDate(value) {
      if (value) {
        return helper.formatDate(value);
      }
      return '';
    },

    formatMessage(item) {
      let message = '';
      if (item.origin === 1) {
        switch (item.status) {
          case 1: message = `${item.report.name} approved`;
            break;
          case 3: message = `${item.report.name} not approved<br/>${item.message}`;
            break;
          default: message = '';
            break;
        }
      } else if (item.origin === 2) {
        switch (item.status) {
          case 1: message = `New comment in ${item.report.name} approved`;
            break;
          default: message = '';
            break;
        }
      }
      return message;
    },

    cleanNotification(item) {
      this.setNotificationRead(item.id).then(() => {
        if (item.origin === 1) {
          if (item.status === 1) {
            this.openReport(item.report.id);
          } else if (item.status === 3) {
            router.push({ name: 'my-reports' });
          }
        }

        if (item.status === 1 && item.origin === 2) {
          this.openReport(item.report.id);
        }
      });
    },

    openReport(id) {
      router.push({
        name: 'project',
        params: {
          path: this.currentProject.path,
        },
      });

      this.setSideBarConfigs({
        tabActived: 'ReportDetail',
        isActived: true,
      }).then(() => {
        this.getReport(id);
      });
    },
  },
};
</script>

<style lang="scss" scoped>
.img {
  width: 20px;
  height: 20px;
  cursor: pointer;
}

.notification-box {
  height: 66px;
  margin-top: 5px;
  z-index: 1;

  .label {
    width: 10px;
    height: 10px;
    background-color: #de486b;
    border-radius: 50%;
    position: absolute;
    padding: 2px 4px;
    margin-left: 23px;
  }

  .notification-item {
    position: absolute;
    background-color: #fff;
    width: 272px;
    height: 290px;
    right: 0;
    box-shadow: 0 0 3px 0 rgba(0, 0, 0, 0.33);
    border-radius: 10px;
    margin: 15px 90px 0px 0px;

    h4 {
      background: #fff;
      height: 40px;
      text-align: center;
      color: #000;
      line-height: 40px;
      font-size: 15px;
      border-radius: 10px 10px 0px 0px;
      margin-bottom: 0px;
    }

    .item {
      width: 100%;
      height: 61px;
      background-color: #fff;
      border-top: solid 0.2px #cbcbcb;

      a {
        display: block;
      }

      .item-left {
        float: left;
        width: 20%;
        padding: 6px 0px 0px 10px;
      }

      .item-right {
        width: 100%;
        font-size: 13px;
        text-align: left;
        padding: 6px 0px 0px 0px;
        margin-left: 10px;
        
        .title {
          color: #4a4a4a;
        }

        small {
          font-size: 10px;
          color: #9b9fa3;
          display: block;
        }
      }
    }

    .thumbnail {
      width: 41px;
      height: 41px;
      border-radius: 4px;
      margin-top: 4px;
    }
  }
}
</style>
