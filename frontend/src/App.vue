<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
/*
 * Root component
 */
export default {
  name: 'App',
};
</script>

<style lang="scss">
  @import "'~bulma/bulma.sass";
  @import './assets/css/base.scss';
</style>
