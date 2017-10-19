<template>
  <div class="header logo">
    <div class="columns is-mobile h-height">
      <div class="column is-3 p-left is-hidden-touch">
        <img class="logo-img" src="~@/assets/img/logo.png">
      </div>
      
      <div class="column project">
        <p class="link" @mouseover.prevent="isVisible = true" @mouseout="isVisible = false">
          {{ currentProject.name }}
          <span class="icon-header-more"></span>
        </p>

        <div class="projects-box" @mouseover.prevent="isVisible = true" @mouseout="isVisible = false" :class="[isVisible ? 'fade-in' : 'fade-out']">
          <div class="item" :key="item.id" v-for="item in projectsList">
            <router-link
              :to="{ name: 'project', params: { path: item.path }}"
              @click.native="openProject(item)">{{ item.name }}
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'Projects',

  data() {
    return {
      isVisible: false,
    };
  },

  computed: {
    ...mapGetters({
      projectsList: 'getAllProjects',
      currentProject: 'getCurrentProject',
    }),
  },

  methods: {
    ...mapActions([
      'setCurrentProject',
      'showDisclaimerProject',
    ]),

    openProject(item) {
      this.setCurrentProject(item);
      this.showDisclaimerProject(true);
    },
  },
};
</script>

<style lang="scss" scoped>
.projects-box {
  position: absolute;
  z-index: 100000;
  max-width: 200px;
  border-radius: 11px;
  background-color: #fff;
  -webkit-box-shadow: 0 0 3px 0 rgba(0, 0, 0, 0.33);
  box-shadow: 0 0 3px 0 rgba(0, 0, 0, 0.33);
  padding: 1px 0px 1px 0px;

  .item {
    height: 38px;
    padding: 6px;
    color: #555555;
    text-align: left;
    border-bottom: solid 0.5px #dddddd;
  }

  .item:last-child {
    border-bottom: none;
  }
}

.header.logo {
  color: #fff;
  height: 78px;

  .p-left {
    text-align: left;
  }

  .logo-img {
    margin-left: 1.5em;
    margin-top: 1em;
  }

  .h-height {
    height: 90px;
  }
}

.project {
  margin-top: 1.5em;
  text-align: left;

  span {
    font-size: 10px;
  }

  p {
    cursor: pointer;
    display: block;
    height: 43px;
    color: #555555;
  }
}
</style>
