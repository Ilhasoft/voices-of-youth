<template>
  <div>
    <img class="is-pulled-right img" src="./../../assets/img/header-search.png" @click.prevent="showInputSearch">
    <input type="text" v-model="inputQuery" v-show="showInput" ref="search" @blur="hiddenInputSearch" />
  </div>
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
  z-index: 1000;
  cursor: pointer;
}
</style>
