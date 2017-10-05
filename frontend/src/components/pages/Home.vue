<template>
  <div>
      <header-index />
      {{ msg }}
      <h4>Links to</h4>
      <intro-project/>
  </div>
</template>

<script>
import HeaderIndex from '../header/Index';
import IntroProject from '../shared/IntroProject';

export default {
  name: 'Home',

  components: { HeaderIndex, IntroProject },

  data() {
    return {
      msg: 'Welcome to Voices of Youth',
    };
  },
};
</script>
