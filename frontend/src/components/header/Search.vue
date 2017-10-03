<template>
  <li class="list-inline-item">
    <input type="search" v-model="inputQuery" v-show="showInput" ref="search" @blur="hiddenInputSearch" />
    <img src="./../../assets/img/header-search.png" @click.prevent="showInputSearch">
  </li>
</template>

<script>
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
    hiddenInputSearch() {
      this.showInput = !this.showInput;
    },

    showInputSearch() {
      this.showInput = !this.showInput;
      this.$nextTick(() => {
        this.$refs.search.focus();
      });
    },
  },
};
</script>

<style lang="scss" scoped>
input {
  width: 236px;
  height: 38px;
  border-radius: 100px;
  border: solid 2px #00cbff;
  outline: none;
  padding: 0px 40px 0px 12px;
}

li {
  margin: 0px !important;
}

img {
  cursor: pointer;
  margin-left: -39px;
}
</style>
