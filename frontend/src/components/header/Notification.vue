<template>
  <li class="list-inline-item">
    <a href="" @click.prevent="showNotifications" @blur="showNotifications">
      <img src="./../../assets/img/header-bell.png">
    </a>

    <div class="notification-box" v-bind:class="[isVisible ? 'fade-in' : 'fade-out']">
      <h4>Notifications</h4>
      <div class="item">
        <a href="">
          <div class="item-left">
            <div class="thumbnail" />
          </div>

          <div class="item-right">
            Steven commented in the report that you posted.
            <small>30 min ago</small>
          </div>
        </a>
      </div>

      <div class="item">
        <a href="">
          <div class="item-left">
            <div class="thumbnail" />
          </div>

          <div class="item-right">
            Steven commented in the report that you posted.
            <small>30 min ago</small>
          </div>
        </a>
      </div>

      <div class="item">
        <a href="">
          <div class="item-left">
            <div class="thumbnail" />
          </div>

          <div class="item-right">
            Steven commented in the report that you posted.
            <small>30 min ago</small>
          </div>
        </a>
      </div>

      <div class="item">
        <a href="">
          <div class="item-left">
            <div class="thumbnail" />
          </div>

          <div class="item-right">
            Steven commented in the report that you posted.
            <small>30 min ago</small>
          </div>
        </a>
      </div>
    </div>
  </li>
</template>

<script>
export default {
  name: 'Notification',

  data() {
    return {
      isVisible: false,
    };
  },

  methods: {
    showNotifications() {
      this.isVisible = !this.isVisible;
    },
  },
};
</script>

<style lang="scss" scoped>
li {
  margin-left: 25px;
}

.notification-box {
  position: absolute;
  background-color: #fff;
  width: 272px;
  height: 290px;
  right: 0;
  box-shadow: 0 0 3px 0 rgba(0, 0, 0, 0.33);
  border-radius: 10px;
  margin-top: 30px;

  >h4 {
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
      width: 80%;
      font-size: 13px;
      text-align: left;
      padding: 6px 0px 0px 0px;
      margin-left: 56px;
      
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
    background-color: #d8d8d8;
    margin-top: 4px;
  }
}

.fade-in {
  visibility: visible;
  opacity: 1;
  transition: opacity 0.2s linear;
}

.fade-out {
  visibility: hidden;
  opacity: 0;
  transition: visibility 0s 0.2s, opacity 0.2s linear;
}
</style>
