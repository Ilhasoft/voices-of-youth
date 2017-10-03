<template>
  <header>
    <div class="header">
      <div class="row">
        <div class="col-md-3">
            <ul class="list-inline">
              <li class="list-inline-item"><img src="./../../assets/img/logo.png"></li>
              <li class="list-inline-item"><a href="">Rio de Janeiro</a></li>
            </ul>
        </div>

        <div class="col-md-6">
            <header-menu />
        </div>

        <div class="col-md-3">
            <right-menu />
        </div>
      </div>
    </div>
    <div class="sub-header"></div>
  </header>
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
ul {
  margin-top: 5px;
}

.header {
  background-color: #fff;
  height: 78.9px;
  width: 100%;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.24);
  -webkit-box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.24);
  padding: 17.5px 37.5px 19.4px 34.3px;
}

.sub-header {
  width: 100%;
  height: 10px;
  background-color: #00cbff;
}

ul>li>a {
  vertical-align: middle;
  margin-left: 36px;
}
</style>
