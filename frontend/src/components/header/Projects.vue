<template>
  <div class="header logo">
    <div class="columns is-mobile h-height">
      <div class="column is-3 p-left"><img class="logo-img" src="./../../assets/img/logo.png"></div>
      <div class="column project">
        <a href="" class="link" @click.prevent="isVisible = true">
          Rio de Janeiro
          <span class="icon-header-more"></span>
        </a>

        <div class="projects-box" @mouseover="isVisible = true" @mouseout="isVisible = false" :class="[isVisible ? 'fade-in' : 'fade-out']">
          <div class="item">
            <a href="">Global - Climate change</a>
          </div>

          <div class="item">
            <a href="">São Paulo</a>
          </div>

          <div class="item">
            <a href="">Global - Religion</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Projects',

  data() {
    return {
      isVisible: false,
    };
  },
};
</script>

<style lang="scss" scoped>
.projects-box {
  max-width: 200px;
  border-radius: 11px;
  background-color: #fff;
  -webkit-box-shadow: 0 0 3px 0 rgba(0, 0, 0, 0.33);
  box-shadow: 0 0 3px 0 rgba(0, 0, 0, 0.33);
  padding: 1px 0px 1px 0px;

  .item {
    height: 38px;
    padding: 6px;
    color: #555555;
    text-align: left;
    border-bottom: solid 0.5px #dddddd;
  }

  .item:last-child {
    border-bottom: none;
  }
}

.header.logo {
  color: #fff;
  height: 78px;

  .p-left {
    text-align: left;
  }

  .logo-img {
    margin-left: 1.5em;
    margin-top: 1em;
  }

  .h-height {
    height: 90px;
  }
}

.project {
  margin-top: 1.5em;
  text-align: left;

  span {
    font-size: 10px;
  }

  .link {
    display: block;
    height: 44px;
  }
}
</style>
