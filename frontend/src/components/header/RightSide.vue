<template>
  <div class="columns is-mobile">
    <search/>
    <notification/>
    <account/>
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
