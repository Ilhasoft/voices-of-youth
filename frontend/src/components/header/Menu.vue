<template>
  <div>
    <div class="columns is-mobile" v-if="showMenu">
      <div class="column"><a href="">Thematics maps</a></div>
      <div class="column"><a href="">Gallery</a></div>
      <div class="column language">
        <a href="">
          Language
          <span class="icon-header-more"></span>
        </a>
      </div>
      
      <div class="column" v-if="userIsLogged"><a href="">My reports</a></div>
      <div class="column new-report" v-if="userIsLogged">
        <a class="button btn-report">
          <span class="icon-header-plus"></span>
          <span> Add report</span>
        </a>
      </div>
    </div>

    <div class="columns is-mobile" v-if="menuTitle && !showMenu">
      <div class="column">{{ menuTitle }}</div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'Menu',

  computed: {
    ...mapGetters({
      userIsLogged: 'userIsLogged',
      showMenu: 'menuIsVisibled',
      menuTitle: 'menuTitle',
    }),
  },
};
</script>

<style lang="scss" scoped>
.language {
  span {
    font-size: 10px;
  }
}

.btn-report {
  border-radius: 100px;
  border: solid 2px #00cbff;
  color: #fff;
  background: #00cbff;
  width: 162px;

  .icon-header-plus {
    font-size: 14px;
    margin-right: 10px;
  }
}

.new-report {
  margin-top: -5px;
}
</style>
