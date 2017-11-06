<template>
  <nav class="pagination is-centered" role="navigation" aria-label="pagination">
    <ul class="pagination-list">
      <li>
        <a @click.prevent="goPreviousPage()" class="pagination-link" :class="cssPreviousPage">
          <svg xmlns="http://www.w3.org/2000/svg" width="21" height="21" viewBox="0 0 21 21">
            <g fill="none" fill-rule="evenodd" transform="translate(.58 .5)">
              <circle cx="10" cy="10" r="10" :fill="colorPrevious"/>
              <path stroke="#FFF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.599 14.18l-4.147-4.146L11.6 5.887"/>
            </g>
          </svg>
        </a>
      </li>
      
      <li :key="key" v-for="(page, key) in pagination">
        <a class="pagination-link" @click.prevent="loadItens(key + 1)" :class="[(key + 1) === currentPage ? 'is-current' : '']" aria-current="page">{{ key + 1 }}</a>
      </li>
      
      <li>
        <a @click.prevent="goNextPage()" class="pagination-link">
          <svg xmlns="http://www.w3.org/2000/svg" width="21" height="21" viewBox="0 0 21 21">
            <g fill="none" fill-rule="evenodd" transform="matrix(-1 0 0 1 20.067 .5)">
              <circle cx="10" cy="10" r="10" :fill="colorNext"/>
              <path stroke="#FFF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.599 14.18l-4.147-4.146L11.6 5.887"/>
            </g>
          </svg>
        </a>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'Pagination',

  props: {
    pagination: {
      type: Number,
      required: true,
    },

    currentPage: {
      type: Number,
      required: true,
    },

    previousPage: {
      type: String,
      required: true,
    },

    nextPage: {
      type: String,
      required: true,
    },
  },

  data() {
    return {
      cssPreviousPage: 'disabled',
      cssNextPage: 'disabled',
      colorPrevious: '#9b9fa3',
      colorNext: '#9b9fa3',
    };
  },

  watch: {
    previousPage() {
      this.cssPreviousPage = (this.previousPage !== '' ? '' : 'disabled');
      this.colorPrevious = (this.previousPage !== '' ? '#00CBFF' : '#9b9fa3');
    },

    nextPage() {
      this.cssNextPage = (this.nextPage !== '' ? '' : 'disabled');
      this.colorNext = (this.nextPage !== '' ? '#00CBFF' : '#9b9fa3');
    },
  },

  methods: {
    goPreviousPage() {
      this.$emit('goPreviousPage', this.currentPage - 1);
    },

    goNextPage() {
      this.$emit('goNextPage', this.currentPage + 1);
    },

    loadItens(page) {
      this.$emit('loadItens', page);
    },
  },
};
</script>

<style lang="scss" scoped>
.pagination {
  margin-bottom: 15px;

  .pagination-link {
    border: none;
    min-width: 10px;
    font-size: 18px;
    letter-spacing: -0.4px;
    text-align: left;
    color: #9b9fa3;

    &.is-current {
      background-color: #f6f6f6;
      color: #000;
    }
  }

  .disabled {
    background-color: none;
    border-color: #dbdbdb;
    -webkit-box-shadow: none;
    box-shadow: none;
    opacity: 0.5;
  }
}
</style>
