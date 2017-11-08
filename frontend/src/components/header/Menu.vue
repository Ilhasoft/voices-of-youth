<template>
  <div>
    <div class="columns is-mobile" v-if="showMenu">
      <div class="column">
        <router-link
          :to="{ name: 'project', params: { path: currentProject.path }}"
          @click.native="openThemes">Themes
        </router-link>
      </div>
      
      <div class="column">
        <router-link
          :to="{ name: 'gallery', params: { path: currentProject.path }}">
          Gallery
        </router-link>
      </div>
      
      <div class="column language">
        <p class="link" @mouseover.prevent="isVisible = true" @mouseout="isVisible = false">
          Language
          <span class="icon-header-more"></span>
        </p>

        <div class="language-box" @mouseover.prevent="isVisible = true" @mouseout="isVisible = false" :class="[isVisible ? 'fade-in' : 'fade-out']">
          <div class="item" :key="key" v-for="(language, key) in menuLanguages">
            <a href="" @click.prevent="setLanguage(language[0])">{{ language[1] }}</a>
          </div>
        </div>
      </div>
      
      <div class="column" v-if="userIsLogged">
        <a href="">My reports</a>
      </div>
      
      <div class="column new-report">
        <router-link
          class="button btn-report"
          :to="{ name: 'newreport', params: { path: currentProject.path }}">
          <span class="icon-header-plus"></span>
          <span> Add report</span>
        </router-link>
      </div>
    </div>

    <div class="columns is-mobile" v-if="menuTitle && !showMenu">
      <div class="column">{{ menuTitle }}</div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'Menu',

  data() {
    return {
      isVisible: false,
    };
  },

  computed: {
    ...mapGetters({
      userIsLogged: 'userIsLogged',
      showMenu: 'menuIsVisibled',
      menuTitle: 'menuTitle',
      menuLanguages: 'getProjectLanguages',
      currentProject: 'getCurrentProject',
    }),
  },

  methods: {
    ...mapActions([
      'setSideBarConfigs',
      'setCurrentLanguage',
    ]),

    openThemes() {
      this.setSideBarConfigs({
        title: 'Themes',
        tabActived: 'Themes',
        backButton: false,
        isActived: true,
      });
    },

    setLanguage(language) {
      this.setCurrentLanguage(language);
    },

    openNewReport() {
      this.setSideBarConfigs({
        title: 'New Report',
        tabActived: 'Themes',
        backButton: false,
        isActived: true,
      });
    },
  },
};
</script>

<style lang="scss" scoped>
.language {
  z-index: 1;

  span {
    font-size: 10px;
  }

  .language-box {
    z-index: 100000;
    position: absolute;
    border-radius: 11px;
    background-color: #fff;
    -webkit-box-shadow: 0 0 3px 0 rgba(0, 0, 0, 0.33);
    box-shadow: 0 0 3px 0 rgba(0, 0, 0, 0.33);
    padding: 1px 0px 1px 0px;

    .item {
      height: 38px;
      padding: 8px;
      color: #555555;
      text-align: left;
      border-bottom: solid 0.5px #dddddd;
    }

    .item:last-child {
      border-bottom: none;
    }
  }

  .link {
    display: block;
    height: 44px;
  }
}

.btn-report {
  border-radius: 100px;
  border: solid 2px #00cbff;
  color: #fff;
  background: #00cbff;
  width: 162px;

  .icon-header-plus {
    font-size: 14px;
    margin-right: 10px;
  }
}

.new-report {
  margin-top: -5px;
}
</style>
