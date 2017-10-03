<template>
  <ul class="list-inline header-rigth-side">
    <search />
    <notification />
    <account />
  </ul>  
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
ul {
  float: right;

  li {
    margin-left: 30px;
  }
}
</style>
