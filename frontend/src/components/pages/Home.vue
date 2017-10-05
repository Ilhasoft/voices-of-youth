<template>
  <div>
      <header-index />
      {{ msg }}
      <router-link to="/project/rio"><h4>Project RIO</h4></router-link>
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
