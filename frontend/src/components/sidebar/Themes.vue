<template>
  <div>
    <navigation-bar
      title="Themes"
      :closeButton="true" />

    <div class="map-box">
      <div class="columns">
        <div class="column scrolling">
          <div class="columns is-mobile">
            <div class="column is-2 filter">
              <div class="field">
                <div class="control">
                  <div class="select is-info">
                    <select v-model="yearStart" @change="getThemesByPeriod">
                      <option :key="key" v-for="(year, key) in currentProject.years">{{ year.substr(0, 4) }}</option>
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
                    <select v-model="yearEnd" @change="getThemesByPeriod">
                      <option :key="key" v-for="(year, key) in currentProject.years">{{ year.substr(0, 4) }}</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>

            <div class="column">
              <div class="control t-right">
              </div>
            </div>
          </div>

          <div class="columns is-mobile item" :key="key" v-for="(item, key) in themesList">
            <div class="column is-2 m-auto center">
              <span class="icon-pin pin" :style="getPinColor(item.color)"></span>
            </div>

            <div class="column m-auto">
              <h1 v-cloak>{{ item.name }}</h1>
              <p v-cloak>{{ getDescription(item.description) }}... <a href="" @click.prevent="openTheme(item)" class="see-more">See more</a></p>
            </div>

            <div class="column is-paddingless is-1 m-auto">
              <checkbox-item :theme-id="item.id" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import bus from '@/helper/bus';
import CheckboxItem from '@/components/shared/Checkbox';
import NavigationBar from './Navigation';

export default {
  name: 'Themes',

  components: { NavigationBar, CheckboxItem },

  data() {
    return {
      isCheckedAll: false,
      yearStart: '',
      yearEnd: '',
    };
  },

  mounted() {
    this.getThemes();

    if (this.currentProject.years.length === 1) {
      this.yearStart = this.currentProject.years[0].substr(0, 4);
      this.yearEnd = this.currentProject.years[0].substr(0, 4);
    }
  },

  computed: {
    ...mapGetters({
      themesList: 'getThemes',
      currentProject: 'getCurrentProject',
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

    getThemesByPeriod() {
      if (this.yearStart && this.yearEnd) {
        this.getThemes({
          yearStart: this.yearStart,
          yearEnd: this.yearEnd,
        });
      }
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
    margin-left: 0px;
    width: 100%;
    padding-left: 30px;
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
