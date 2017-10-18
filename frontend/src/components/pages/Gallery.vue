<template>
  <div>
    <header-index/>
    <div class="page-container">
      <nav class="pagination is-centered" role="navigation" aria-label="pagination">
        <ul class="pagination-list">
          <li>
            <a class="pagination-link" aria-label="Goto page 1">
              <svg xmlns="http://www.w3.org/2000/svg" width="21" height="21" viewBox="0 0 21 21">
                <g fill="none" fill-rule="evenodd" transform="translate(.58 .5)">
                  <circle cx="10" cy="10" r="10" fill="#00CBFF"/>
                  <path stroke="#FFF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.599 14.18l-4.147-4.146L11.6 5.887"/>
                </g>
              </svg>
            </a>
          </li>
          <li><a class="pagination-link is-current" aria-label="Page 1" aria-current="page">1</a></li>
          <li><a class="pagination-link" aria-label="Goto page 45">2</a></li>
          <li><a class="pagination-link" aria-label="Goto page 45">3</a></li>
          <li><a class="pagination-link" aria-label="Goto page 45">4</a></li>
          <li><a class="pagination-link" aria-label="Goto page 45">5</a></li>
          <li><a class="pagination-link" aria-label="Goto page 45">6</a></li>
          <li>
            <a class="pagination-link" aria-label="Goto page 86">
              <svg xmlns="http://www.w3.org/2000/svg" width="21" height="21" viewBox="0 0 21 21">
                <g fill="none" fill-rule="evenodd" transform="matrix(-1 0 0 1 20.067 .5)">
                  <circle cx="10" cy="10" r="10" fill="#00CBFF"/>
                  <path stroke="#FFF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.599 14.18l-4.147-4.146L11.6 5.887"/>
                </g>
              </svg>
            </a>
          </li>
        </ul>
      </nav>

      <div class="columns" :key="key" v-for="(value, key) in items">
        <div class="column" :key="key" v-for="(value, key) in items">
          <div class="card">
            <div class="card-image">
              <figure class="image">
                <img v-bind:src="getImgUrl(key)" alt="">
              </figure>
            </div>
            
            <div class="card-content">
              <div class="media">
                <div class="media-content">
                  <p class="title">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod…</p>
                  <p class="subtitle">Avada Lorem ipsum dolor sit amet, conse adipiscing elit, sed do eiusmod…</p>
                </div>
            </div>

            <div class="content">
              <img src="~@/assets/img/login-a.png" class="avatar" alt="">
              <small>Bradley Evans</small>
            </div>
          </div>
        </div>
      </div>
    </div>

    <nav class="pagination is-centered" role="navigation" aria-label="pagination">
      <ul class="pagination-list">
        <li>
          <a class="pagination-link" aria-label="Goto page 1">
            <svg xmlns="http://www.w3.org/2000/svg" width="21" height="21" viewBox="0 0 21 21">
              <g fill="none" fill-rule="evenodd" transform="translate(.58 .5)">
                <circle cx="10" cy="10" r="10" fill="#00CBFF"/>
                <path stroke="#FFF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.599 14.18l-4.147-4.146L11.6 5.887"/>
              </g>
            </svg>
          </a>
        </li>
        <li><a class="pagination-link is-current" aria-label="Page 1" aria-current="page">1</a></li>
        <li><a class="pagination-link" aria-label="Goto page 45">2</a></li>
        <li><a class="pagination-link" aria-label="Goto page 45">3</a></li>
        <li><a class="pagination-link" aria-label="Goto page 45">4</a></li>
        <li><a class="pagination-link" aria-label="Goto page 45">5</a></li>
        <li><a class="pagination-link" aria-label="Goto page 45">6</a></li>
        <li>
          <a class="pagination-link" aria-label="Goto page 86">
            <svg xmlns="http://www.w3.org/2000/svg" width="21" height="21" viewBox="0 0 21 21">
              <g fill="none" fill-rule="evenodd" transform="matrix(-1 0 0 1 20.067 .5)">
                <circle cx="10" cy="10" r="10" fill="#00CBFF"/>
                <path stroke="#FFF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.599 14.18l-4.147-4.146L11.6 5.887"/>
              </g>
            </svg>
          </a>
        </li>
      </ul>
    </nav>
  </div>
</div>
</template>

<script>
import HeaderIndex from '../header/Index';

export default {
  name: 'Gallery',

  components: { HeaderIndex },

  data() {
    return {
      items: [1, 2, 3, 4, 5, 6],
    };
  },

  beforeCreate: () => {
    document.body.className = 'grey';
  },

  beforeDestroy: () => {
    document.body.className = 'white';
  },

  methods: {
    getImage() {
      return '../../assets/img/gallery-1.png';
    },

    getImgUrl(id) {
      const images = require.context('../../assets/img/', false, /\.png$/);
      return images(`./gallery-${id}.png`);
    },
  },
};
</script>

<style lang="scss" scoped>
.page-container {
  margin: auto;
  padding: 20px 67px;

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
  }

  .card {
    border-radius: 10px;
    box-shadow: none;

    figure {
      display: table;
      margin: auto;
    }
  }

  .image img {
    max-width: 100%;
  }

  .title {
    font-size: 18px;
    font-weight: 500;
    letter-spacing: -0.5px;
    text-align: left;
    color: #000000;
    margin-bottom: 1px;
  }

  .subtitle {
    margin: 10px 0px 5px;
    font-size: 14px;
    letter-spacing: -0.3px;
    text-align: left;
    color: #000000;
  }

  .avatar {
    width: 25px;
    height: 25px;
    float: left;
    margin-right: 5px;
  }

  .image {
    padding: 12px;
  }

  small {
    font-size: 14px;
    letter-spacing: -0.4px;
    text-align: left;
    color: #000000;
  }
}
</style>
