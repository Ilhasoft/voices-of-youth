<template>
  <div class="columns is-mobile">
    <div class="column"><a href="">Thematics maps</a></div>
    <div class="column"><a href="">Gallery</a></div>
    <div class="column"><a href="">Language</a></div>
    <div class="column"><a href="">My reports</a></div>
    <div class="column new-report">
      <a class="button btn-report">
        <span class="icon-header-plus"></span>
        <span> Add report</span>
      </a>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Menu',
};
</script>

<style lang="scss" scoped>
.btn-report {
  border-radius: 100px;
  border: solid 2px #00cbff;
  color: #fff;
  background: #00cbff;
  width: 162px;

  .icon-header-plus {
    font-size: 14px;
    margin-right: 10px;
  }
}

.new-report {
  margin-top: -5px;
}
</style>
