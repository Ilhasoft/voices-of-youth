<template>
  <ul class="list-inline">
    <li class="list-inline-item"><a href="">Thematics maps</a></li>
    <li class="list-inline-item"><a href="">Gallery</a></li>
    <li class="list-inline-item"><a href="">Language</a></li>
    <li class="list-inline-item"><a href="">My reports</a></li>
    <li class="list-inline-item li-new-report">
      <a href="" class="btn-report">Add report</a>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'Menu',
};
</script>

<style lang="scss" scoped>
ul {
  text-align: center;
  margin-top: 5px;
}

li {
  height: 40px;
  min-width: 15%;
}

a {
  vertical-align: middle;
}

.li-new-report {
  width: 180px;
}

.btn-report {
  border-radius: 100px;
  border: solid 2px #00cbff;
  color: #fff;
  display: block;
  width: 162px;
  height: 38px;
  line-height: 34px;
  background: #00cbff url('./../../assets/img/header-plus.png') no-repeat 21px 10px;
}
</style>
