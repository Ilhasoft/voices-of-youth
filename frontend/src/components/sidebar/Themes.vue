<template>
  <div class="map-box">
    <div class="columns">
      <div class="column scrolling">
        <div class="columns is-mobile">
          <div class="column is-2 filter">
            <div class="field">
              <div class="control">
                <div class="select is-info">
                  <select>
                    <option>2017</option>
                    <option>2016</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          <div class="column is-1 m-auto">
            <p>to</p>
          </div>

          <div class="column is-2 filter">
            <div class="field">
              <div class="control">
                <div class="select is-info">
                  <select>
                    <option>2017</option>
                    <option>2016</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          <div class="column">
            <div class="control t-right">
              <label class="radio">
                Select all &nbsp;&nbsp;
                <svg @click.prevent="setCheckAll(false)" v-if="isCheckedAll" xmlns="http://www.w3.org/2000/svg" width="23" height="21" viewBox="0 0 23 21">
                  <g fill="none" fill-rule="evenodd" stroke="#00D3C2" stroke-linecap="round" stroke-linejoin="round" stroke-width="2">
                    <path d="M7.418 9.404l3.01 3 11.037-11"/>
                    <path d="M19.458 10.404v7c0 1.105-.898 2-2.007 2H3.405a2.003 2.003 0 0 1-2.006-2v-14c0-1.104.898-2 2.006-2h11.036"/>
                  </g>
                </svg>
                <svg @click.prevent="setCheckAll(true)" v-else xmlns="http://www.w3.org/2000/svg" width="21" height="21" viewBox="0 0 21 21">
                  <rect width="18" height="18" fill="none" fill-rule="evenodd" stroke="#AFAFAF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" rx="2" transform="translate(1.399 1.602)"/>
                </svg>
              </label>
            </div>
          </div>
        </div>

        <div class="columns is-mobile item" :key="key" v-for="(item, key) in themesList">
          <div class="column is-1 m-auto center">
            <span class="icon-pin pin" :style="getPinColor(item.color)"></span>
          </div>

          <div class="column m-auto">
            <h1>{{ item.name }}</h1>
            <p>{{ getDescription(item.description) }}... <a href="" @click.prevent="openTheme(item)" class="see-more">See more</a></p>
          </div>

          <div class="column is-1 m-auto">
            <checkbox-item :theme-id="item.id" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import bus from '../../helper/bus';
import CheckboxItem from '../shared/Checkbox';

export default {
  name: 'Themes',

  components: { CheckboxItem },

  data() {
    return {
      isCheckedAll: false,
    };
  },

  mounted() {
    this.getThemes();
  },

  computed: {
    ...mapGetters({
      themesList: 'getThemes',
    }),
  },

  methods: {
    ...mapActions([
      'getThemes',
      'getTheme',
      'setSideBarConfigs',
      'getReports',
      'getReportsByTheme',
      'clearReports',
    ]),

    setCheckAll(value) {
      this.isCheckedAll = value;
      bus.$emit('checkAllThemes', value);
      this.clearReports();
      this.getReports();
    },

    getPinColor(color) {
      return `color: #${color}`;
    },

    getDescription(descrition) {
      if (descrition) {
        const trimmedString = descrition.substr(0, 118);
        return trimmedString.substr(0, Math.min(trimmedString.length, trimmedString.lastIndexOf(' ')));
      }
      return '';
    },

    openTheme(item) {
      this.setSideBarConfigs({
        title: 'Themes',
        tabActived: 'Theme',
        backButton: true,
        backTo: 'Themes',
        isActived: true,
      }).then(() => {
        this.getTheme(item.id);
      });
    },
  },
};
</script>

<style lang="scss" scoped>
.map-box {
  margin: auto;
  padding-left: 25px;

  .filter {
    width: 20% !important;
  }

  .t-right {
    text-align: right;
    margin-right: 12px;
  }

  .item {
    margin-top: 15px;
    margin-bottom: 15px;
    width: 100%;
    min-height: 125px;
    border-radius: 10px;
    background-color: #fff;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.16);
  }

  .scrolling {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    overflow-y: scroll;
    margin-top: 62px;
    margin-left: 20px;
    min-width: 602px;
  }

  .m-auto {
    margin: auto;
  }

  .pin {
    font-size: 38px;
    color: #9013fe;
  }

  .center {
    text-align: center;
  }

  h1 {
    font-size: 18px;
    font-weight: bold;
    letter-spacing: -0.5px;
    text-align: left;
    color: #000000;
  }

  p {
    font-size: 15px;
    line-height: 1.33;
    letter-spacing: -0.4px;
    text-align: left;
    color: #000000;
  }

  .see-more {
    color: #00cbff;
  }
}
</style>
