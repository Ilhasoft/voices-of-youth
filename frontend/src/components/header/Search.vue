<template>
  <div class="column has-text-right">
    <img class="is-pulled-right img" src="~@/assets/img/header-search.png" @click.prevent="showInputSearch">
    <input type="text" v-model="inputQuery" v-show="showInput" @keyup.enter="search" ref="search" @blur="showInput = false" />
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: 'ItemSearch',

  data() {
    return {
      inputQuery: '',
      inputClass: '',
      showInput: false,
    };
  },

  methods: {
    ...mapActions([
      'searchReports',
      'setSideBarConfigs',
    ]),

    showInputSearch() {
      this.showInput = true;
      this.$nextTick(() => {
        this.$refs.search.focus();
      });
    },

    search() {
      this.searchReports(this.inputQuery).then(() => {
        this.setSideBarConfigs({
          title: 'Results',
          tabActived: 'Search',
          backButton: false,
          isActived: true,
        });
      });
    },
  },
};
</script>

<style lang="scss" scoped>
input {
  width: 100%;
  height: 38px;
  border-radius: 100px;
  border: solid 2px #00cbff;
  outline: none;
  padding: 0px 40px 0px 12px;
  margin-top: -5px;
  position: relative;
}

.img {
  margin-top: 5px;
  width: 20px;
  height: 20px;
  position: absolute;
  cursor: pointer;
}
</style>
