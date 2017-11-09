<template>
  <div id="app">
    <notify />
    <router-view></router-view>
  </div>
</template>

<script>
/*
 * Root component
 */
import Notify from './components/shared/Notify';

export default {
  name: 'App',

  components: { Notify },
};
</script>

<style lang="scss">
  @import "'~bulma/bulma.sass";
  @import './assets/css/base.scss';
</style>
