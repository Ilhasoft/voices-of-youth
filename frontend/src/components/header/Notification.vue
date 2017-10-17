<template>
  <div class="column is-2 notification-box" @mouseover.prevent="isVisible = true" @mouseout="isVisible = false">
    <a href="">
      <img class="img" src="./../../assets/img/header-bell.png">
    </a>

    <div class="notification-item" @mouseover.prevent="isVisible = true" @mouseout="isVisible = false" :class="[isVisible ? 'fade-in' : 'fade-out']">
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
  </div>
</template>

<script>
export default {
  name: 'Notification',

  data() {
    return {
      isVisible: false,
    };
  },
};
</script>

<style lang="scss" scoped>
.img {
  width: 20px;
  height: 20px;
}

.notification-box {
  height: 66px;
  margin-top: 5px;

  .notification-item {
    position: absolute;
    background-color: #fff;
    width: 272px;
    height: 290px;
    right: 0;
    box-shadow: 0 0 3px 0 rgba(0, 0, 0, 0.33);
    border-radius: 10px;
    margin: 15px 10px 0px 0px;

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
}
</style>
