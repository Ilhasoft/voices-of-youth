<template>
  <div>
    <div class="header">
      <div class="container">
        <div class="columns is-marginless is-paddingless header">
          <div class="column is-offset-1">
            <img src="~@/assets/img/logo-home.png" alt="">
          </div>
        </div>
      </div>
    </div>

    <div class="container">
      <div class="columns is-marginless">
        <div class="column is-12 is-offset-1">
          <div class="nav">
            <router-link :to="{ name: 'home' }">Home</router-link>&nbsp;&gt;&nbsp;All projects
          </div>
          <h4>All projects</h4>
          <div class="columns">
            <div class="column is-10 projects">
              <div class="project" v-for="(project, key) in projects" :key="key">
                <div class="columns">
                  <div class="column">
                    <a href="" @click.prevent="openProject(project)">
                      <div class="columns is-mobile">
                        <div class="column is-2">
                          <img :src="project.thumbnail" v-if="project.thumbnail" alt="" />
                        </div>
                        <div class="column no-pad-l text">
                          <h1>{{ project.name }}</h1>
                          <p>{{ project.description }}</p>
                        </div>
                      </div>
                    </a>
                  </div>
                </div>
              </div>
              <div v-if="next" class="has-text-centered show-more">
                <a href="" @click.prevent="showMore">Show more</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import router from '@/router/';

export default {
  name: 'Projects',

  data() {
    return {
      projects: [],
      page: 0,
      next: '',
    };
  },

  mounted() {
    this.getProjects(1);
  },

  methods: {
    ...mapActions([
      'getHomeProjects',
      'setCurrentProject',
      'showDisclaimerProject',
    ]),

    showMore() {
      if (this.next) {
        this.getProjects(this.page + 1);
      }
    },

    getProjects(currentPage) {
      this.getHomeProjects({ pageSize: 2, page: currentPage }).then((projects) => {
        this.page = currentPage;
        this.next = projects.next;
        projects.results.map(item => this.projects.push(item));
      });
    },

    openProject(item) {
      this.setCurrentProject(item).then(() => {
        router.push({ name: 'project', params: { path: item.path } });
        this.showDisclaimerProject(true);
      });
    },
  },
};
</script>

<style lang="scss" scoped>
@import url('https://fonts.googleapis.com/css?family=Roboto:400,500');

.header {
  background-color: #009ee3;
  width: 100%;
}

.container {
  font-family: 'Roboto';
  font-weight: 400;

  .nav {
    font-size: 14px;
    font-weight: 500;
    color: #4a4a4a;
    margin-top: 27px;

    a {
      color: #4a90e2;
    }
  }

  h4 {
    font-size: 40px;
    font-weight: bold;
    color: #000000;
  }

  .no-pad-l {
    padding-left: 0px;
  }

  .show-more a {
    font-size: 18px;
    color: #4a90e2;
  }

  .projects {
    margin-top: 41px;

    .project {
      min-height: 163px;
      width: 100%;
      background-color: #ffffff;
      border: 1px solid #c3c3c3;
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 14px;

      h1 {
        font-size: 25px;
        font-weight: 500;
        color: #000000;
        text-align: left;
      }

      p {
        font-size: 14px;
        color: #000000;
      }
    }
  }
}
</style>
