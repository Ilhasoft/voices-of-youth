<template>
  <div>
    <header-index />
    PROJECT RIO

    <router-link to="/login"><h4>LOGIN</h4></router-link>
    <router-link to="/profile"><h4>PROFILE</h4></router-link>
    <router-link to="/my-reports"><h4>MY REPORTS</h4></router-link>
    <router-link to="/project/rio/gallery"><h4>GALLERY</h4></router-link>
  </div>
</template>

<script>
import HeaderIndex from '../header/Index';

export default {
  name: 'Project',

  components: { HeaderIndex },
};
</script>
