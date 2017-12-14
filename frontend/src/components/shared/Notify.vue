<template>
  <div class="notify" :class="isVisible">
    <div class="alert" :class="cssAlert">
      <a class="close" @click.prevent="close()">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
          <g fill="none" fill-rule="evenodd" stroke="#FFF" stroke-linecap="round" stroke-linejoin="round" stroke-width="4">
            <path d="M13.266 2.21L2.142 13.334M2.142 2.21l11.124 11.124"/>
          </g>
        </svg>
      </a>
      <div class="text">{{ notifyInfo.message }}</div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'Notify',

  computed: {
    ...mapGetters({
      notifyInfo: 'getNotifyInfo',
    }),

    cssAlert() {
      return this.notifyInfo.type === 1 ? 'alert-success' : 'alert-danger';
    },

    isVisible() {
      return this.notifyInfo.visible ? 'fade-in' : 'fade-out';
    },
  },

  watch: {
    isVisible() {
      if (this.isVisible === 'fade-in') {
        setTimeout(() => {
          this.close();
        }, 4000);
      }
    },
  },

  methods: {
    ...mapActions([
      'notifyClose',
    ]),

    close() {
      this.notifyClose();
    },
  },
};
</script>

<style lang="scss" scoped>
.notify {
  position: fixed;
  top: 78px;
  z-index: 1040;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
  width: 350px;
  left: auto;
  right: 0px;
  -webkit-animation-duration: 1s;
  animation-duration: 1s;
  -webkit-animation-fill-mode: both;
  animation-fill-mode: both;

  .alert {
    // height: 53px;
    color: #fff;
    padding: 16px;
    margin-bottom: 21px;
    border: 1px solid transparent;
    border-radius: 3px;

    .close {
      margin-top: 3px;
      float: right;
      cursor: pointer;
    }

    .text {
      font-size: 16px;
      font-weight: 500;
      letter-spacing: -0.4px;
      text-align: left;
      color: #ffffff;
    }
  }

  .alert-danger {
    background-color: #f05050;
    border-color: rgba(0,0,0,.1);
  }

  .alert-success {
    background-color: #27c24c;
    border-color: rgba(0,0,0,.1);
  }
}

@-webkit-keyframes fade-in {
  0% {opacity: 0;}
  100% {opacity: 1;}
}

@keyframes fade-in {
  0% {opacity: 0;}
  100% {opacity: 1;}
}

.fade-in {
  -webkit-animation-name: fade-in;
  animation-name: fade-in;
}

@-webkit-keyframes fade-out {
  0% {opacity: 1;}
  100% {opacity: 0;}
}

@keyframes fade-out {
  0% {opacity: 1;}
  100% {opacity: 0;}
}

.fade-out {
  -webkit-animation-name: fade-out;
  animation-name: fade-out;
}
</style>

