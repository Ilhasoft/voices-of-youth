<template>
  <small>
    <svg @click.prevent="setChecked" v-if="isChecked" xmlns="http://www.w3.org/2000/svg" width="23" height="21" viewBox="0 0 23 21">
        <g fill="none" fill-rule="evenodd" stroke="#00D3C2" stroke-linecap="round" stroke-linejoin="round" stroke-width="2">
          <path d="M7.418 9.404l3.01 3 11.037-11"/>
          <path d="M19.458 10.404v7c0 1.105-.898 2-2.007 2H3.405a2.003 2.003 0 0 1-2.006-2v-14c0-1.104.898-2 2.006-2h11.036"/>
        </g>
    </svg>
    <svg @click.prevent="setChecked" v-else xmlns="http://www.w3.org/2000/svg" width="21" height="21" viewBox="0 0 21 21">
      <rect width="18" height="18" fill="none" fill-rule="evenodd" stroke="#AFAFAF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" rx="2" transform="translate(1.399 1.602)"/>
    </svg>
  </small>
</template>

<script>
import { mapActions } from 'vuex';
import bus from '../../helper/bus';

export default {
  name: 'Checkbox',

  props: {
    themeId: {
      type: Number,
      required: false,
    },
  },

  data() {
    return {
      isChecked: false,
    };
  },

  mounted() {
    bus.$on('checkAllThemes', (e) => {
      this.isChecked = e;
    });
  },

  methods: {
    ...mapActions([
      'getReportsByTheme',
    ]),

    setChecked() {
      this.isChecked = !this.isChecked;
      this.getReport();
    },

    getReport() {
      this.getReportsByTheme({
        isChecked: this.isChecked,
        themeId: this.themeId,
      });
    },
  },
};
</script>

<style lang="scss" scoped>
small {
  cursor: pointer;
}

.checkbox {
  display: none;
}
</style>

