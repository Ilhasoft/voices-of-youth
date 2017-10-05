<template>
  <div class="header logo">
    <div class="columns is-mobile">
      <div class="column is-3 p-left"><img class="logo-img" src="./../../assets/img/logo.png"></div>
      <div class="column project">
        <a href="">
          Rio de Janeiro
          <span class="icon-header-more"></span>
        </a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Projects',
};
</script>

<style lang="scss" scoped>
.p-left {
  text-align: left;
}

.header.logo {
  color: #fff;
  height: 78px;

  .logo-img {
    margin-left: 1.5em;
    margin-top: 1em;
  }
}

.project {
  margin-top: 1.5em;
  text-align: left;

  span {
    font-size: 10px;
  }
}
</style>
