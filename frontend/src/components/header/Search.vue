<template>
  <div class="column is-6 has-text-right">
    <input
        type="text"
        :placeholder="$t('message.header.search.input')"
        :value="searchQuery"
        @input="updateQuery"
        @keyup.enter="search"
        ref="search" />
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'ItemSearch',

  data() {
    return {
      inputClass: '',
      showInput: false,
    };
  },

  computed: {
    ...mapGetters(['searchQuery']),
  },

  methods: {
    ...mapActions([
      'searchReports',
      'setSideBarConfigs',
      'setSearchQuery',
    ]),

    updateQuery(event) {
      const value = event.target.value;
      this.setSearchQuery(value);
    },

    showInputSearch() {
      this.showInput = true;
      this.$nextTick(() => {
        this.$refs.search.focus();
      });
    },

    search() {
      this.searchReports(this.searchQuery).then(() => {
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
