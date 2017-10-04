<template>
  <div class="columns is-mobile">
    <div class="column has-text-right-desktop">
      <search/>
    </div>
    <div class="column is-2 m-top">
      <notification/>
    </div>
    <div class="column is-2 is-paddingless m-right m-top">
      <account/>
    </div>
  </div>
</template>

<script>
import Search from './Search';
import Notification from './Notification';
import Account from './Account';

export default {
  name: 'RightSide',

  components: { Search, Notification, Account },
};
</script>

<style lang="scss" scoped>
.m-right {
  margin-right: 20px;
}

.m-top {
  margin-top: 5px;
}
</style>
