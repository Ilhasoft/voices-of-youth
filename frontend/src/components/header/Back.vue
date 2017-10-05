<template>
  <div class="p-left">
    <div class="columns is-mobile p-top">
      <div class="column is-2">
        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="24" viewBox="0 0 25 24">
          <g fill="none" fill-rule="evenodd" stroke="#00CBFF" stroke-linecap="round" stroke-linejoin="round" stroke-width="4">
            <path d="M22.68 11.676H3.264M12.052 21.38l-9.705-9.704 9.705-9.706"/>
          </g>
        </svg>
      </div>
      <div class="column t-align">
        <a href="#" onclick="window.history.back();">Back to map</a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BackButton',
};
</script>

<style lang="scss" scoped>
.t-align {
  text-align: left;

  a {
    font-size: 18px;
    font-weight: 500;
    letter-spacing: -0.4px;
  }
}

.p-top {
  padding-top: 20px;
}

.p-left {
  padding-left: 102px;
}

.header {
  vertical-align: middle;
  position: relative;
  text-align: center;
  font-size: 18px;
  font-weight: 500;
  letter-spacing: -0.4px;

  p {
    padding-top: 22px;
  }
}
</style>
