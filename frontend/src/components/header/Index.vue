<template>
  <section>
    <div class="columns">
      <div class="column is-3">
        <div class="header logo">
          <div class="columns is-mobile">
            <div class="column is-3 p-left"><img class="logo-img" src="./../../assets/img/logo.png"></div>
            <div class="column project">
              <a href="">
                Rio de Janeiro
                <span class="icon-header-more"></span>
              </a>
            </div>
          </div>
        </div>
      </div>
  
      <div class="column">
        <div class="header menu">
          <header-menu />
        </div>
      </div>

      <div class="column is-3">
        <div class="header account">
          <right-menu />
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import HeaderMenu from './Menu';
import RightMenu from './RightSide';

export default {
  name: 'Index',

  components: { HeaderMenu, RightMenu },
};
</script>

<style lang="scss" scoped>
section {
  border-bottom: 12px solid #00cbff;
}

.p-left {
  text-align: left;
}

.project {
  margin-top: 1.5em;
  text-align: left;

  span {
    font-size: 10px;
  }
}

.header.logo {
  color: #fff;
  height: 78px;

  .logo-img {
    margin-left: 1.5em;
    margin-top: 1em;
  }
}

.header.menu {
  height: 66px;
  padding-top: 22px;
}

.header.account {
  color: rgba(0, 0, 0, 0.7);
  height: 66px;
  padding: 1.25rem 0;
}

.header {
  vertical-align: middle;
  position: relative;
  text-align: center;
}
</style>
