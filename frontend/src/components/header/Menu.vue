<template>
  <div>
    <div class="columns is-mobile" v-if="showMenu">
      <div class="column">
        <router-link
          :to="{ name: 'project', params: { path: currentProject.path }}"
          @click.native="openThemes">{{ $t('message.header.themes') }}
        </router-link>
      </div>
      
      <div class="column">
        <router-link
          :to="{ name: 'gallery', params: { path: currentProject.path }}">
          {{ $t('message.header.gallery') }}
        </router-link>
      </div>
      
      <div class="column language">
        <a href="" class="link" @mouseover.prevent="isVisible = true" @mouseout="isVisible = false">
          {{ $t('message.header.language') }}
          <span class="icon-header-more"></span>
          <div class="language-box" @mouseover.prevent="isVisible = true" @mouseout="isVisible = false" :class="[isVisible ? 'fade-in' : 'fade-out']">
            <div class="item" :key="key" v-for="(language, key) in menuLanguages">
              <a href="" @click.prevent="setLanguage(language[0])">{{ language[1] }}</a>
            </div>
          </div>
        </a>
      </div>
      
      <div class="column" v-if="userIsLogged && userIsMapper">
        <router-link
          :to="{ name: 'my-reports' }">{{ $t('message.header.myreports') }}
        </router-link>
      </div>
      
      <div class="column new-report" v-if="userIsLogged && userIsMapper && themes.length > 0">
        <router-link
          class="button btn-report"
          :to="{ name: 'newreport', params: { path: currentProject.path }}">
          <span class="icon-header-plus"></span>
          <span> {{ $t('message.header.btnAddReport') }}</span>
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
      defaultLang: [
        ['en', 'English'],
        // ['fr', 'French'],
        // ['es', 'Spanish'],
        // ['pt-br', 'Portuguese'],
        // ['ar', 'Arabic'],
      ],
    };
  },

  computed: {
    ...mapGetters({
      userIsLogged: 'userIsLogged',
      userIsMapper: 'userIsMapper',
      showMenu: 'menuIsVisibled',
      menuTitle: 'menuTitle',
      currentProject: 'getCurrentProject',
      currentUser: 'getUserData',
      themes: 'getMyThemes',
    }),

    menuLanguages() {
      const languages = [...this.defaultLang, ...this.$store.getters.getProjectLanguages];
      return languages.filter(
        (elem, pos, arr) => arr.map(
          mapObj => mapObj[0]).indexOf(elem[0]) === pos);
    },
  },

  mounted() {
    this.getMyThemesByProject();
  },

  methods: {
    ...mapActions([
      'setSideBarConfigs',
      'setCurrentLanguage',
      'getMyThemesByProject',
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
    border-radius: 11px;
    background-color: #fff;
    -webkit-box-shadow: 0 0 3px 0 rgba(0, 0, 0, 0.33);
    box-shadow: 0 0 3px 0 rgba(0, 0, 0, 0.33);
    padding: 1px 0px 1px 0px;
    margin-top: 20px;

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

    a {
      display: block;
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
  width: 125px;

  .icon-header-plus {
    font-size: 14px;
    margin-right: 10px;
  }
}

.new-report {
  margin-top: -5px;
}
</style>
