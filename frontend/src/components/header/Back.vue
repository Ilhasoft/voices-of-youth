<template>
  <div class="p-left">
    <div class="columns p-top">
      <div class="column is-2">
        <a href="#" onclick="window.history.back();">
          <svg xmlns="http://www.w3.org/2000/svg" width="25" height="24" viewBox="0 0 25 24">
            <g fill="none" fill-rule="evenodd" stroke="#00CBFF" stroke-linecap="round" stroke-linejoin="round" stroke-width="4">
              <path d="M22.68 11.676H3.264M12.052 21.38l-9.705-9.704 9.705-9.706"/>
            </g>
          </svg>
        </a>
      </div>
      <div class="column t-align is-hidden-touch">
        <router-link
          :to="{ name: 'project', params: { path: currentProject.path }}">
          Back to map
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'BackButton',

  computed: {
    ...mapGetters({
      currentProject: 'getCurrentProject',
    }),
  },
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
