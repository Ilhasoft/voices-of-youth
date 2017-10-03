<template>
  <div>
      <header-index />
      {{ msg }}
      <h4>Links to</h4>
  </div>
</template>

<script>
import HeaderIndex from '../header/Index';

export default {
  name: 'Home',

  components: { HeaderIndex },

  data() {
    return {
      msg: 'Welcome to Voices of Youth',
    };
  },
};
</script>
