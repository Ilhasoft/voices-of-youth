<template>
  <div class="columns links">
    <div class="column is-10">
      <p class="left">sdf</p>
    </div>

    <div class="column right" @mouseover="isVisible = true" @mouseout="isVisible = false">
      <span class="icon-icon-more more">
        <div class="actions" :class="[isVisible ? 'fade-in' : 'fade-out']">
          <p><a>Edit</a></p>
          <p><a>Remove</a></p>
        </div>
      </span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Link',

  data() {
    return {
      isVisible: false,
    };
  },
};
</script>

<style lang="scss" scoped>
.links {
  .left {
    width: 100%;
    height: 36px;
    border-radius: 4px;
    background-color: #ffffff;
    margin: auto;
    padding-top: 8px;
    padding-left: 8px;
    border: 1px solid rgba(60,60,60,.26);
  }

  .right {
    position: relative;
    text-align: center;
    margin: auto;
  }

  .more {
    font-size: 24px;
    z-index: 10;
  }

  .actions {
    width: 83px;
    height: 79px;
    border-radius: 5px;
    background-color: #fff;
    box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.14);
    text-align: left;
    position: absolute;
    margin-top: -38px;
    margin-left: -15px;
    cursor: pointer;

    p {
      margin-left: 15px;
      padding-top: 10px;
    }

    a {
      font-size: 14px;
      letter-spacing: -0.3px;
      text-align: center;
      color: #4a4a4a;
    }
  }
}
</style>
