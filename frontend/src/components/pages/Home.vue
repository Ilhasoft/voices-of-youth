<template>
  <div>
    <div class="header">
      <div class="header-info container">
        <div class="columns is-marginless">
          <div class="column is-5 m-auto">
            <h1>Visualizing Risk and Resilience</h1>
            <small>A UNICEF Mobile and Web Digital Mapping Solution</small>
            <p>This project explores tools to help youth build impactful, communicative digital maps using mobile and web technologies. A phone application allows youth to produce a portrait of their community through geo-located photos and videos, organized in thematic maps.</p>
          </div>

          <div class="column is-5 m-auto">
            <img src="~@/assets/img/home.png" class="img-home" alt="">
          </div>
        </div>
      </div>
    </div>

    <div class="body container">
      <h1>Projects</h1>

      <div class="columns is-marginless m-bottom" :key="item.id" v-for="item in projectsList">
        <div class="column is-2 is-paddingless image">
          <img :src="item.thumbnail_cropped" v-if="item.thumbnail_cropped" alt="" />
        </div>

        <div class="column is-marginless p-top">
          <h2>{{ item.name }}</h2>
          <small>{{ item.description }}</small>
          <a href="" @click.prevent="openProject(item)" class="button">See more</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import router from '@/router/';

export default {
  name: 'Home',

  mounted() {
    this.setProjects();
  },

  computed: {
    ...mapGetters({
      projectsList: 'getAllProjects',
    }),
  },

  methods: {
    ...mapActions([
      'setProjects',
      'setCurrentProject',
      'showDisclaimerProject',
    ]),

    openProject(item) {
      this.setCurrentProject(item).then(() => {
        router.push({ name: 'project', params: { path: item.path } });
        this.showDisclaimerProject(true);
      });
    },
  },

  beforeCreate: () => {
    document.body.className = 'home';
  },
};
</script>

<style lang="scss" scoped>
.header {
  width: 100%;
  background-color: #00cbff;
  padding-top: 70px;

  .m-auto {
    margin: auto;
  }

  .header-info {
    margin: auto;
    background-color: #00cbff;

    h1 {
      line-height: normal;
      font-size: 50px;
      font-weight: bold;
      letter-spacing: -1.3px;
      text-align: left;
      color: #fff;
    }

    small {
      font-size: 25px;
      letter-spacing: -0.6px;
      text-align: left;
      color: #fff;
    }

    p {
      margin-top: 25px;
      font-size: 15px;
      line-height: 1.67;
      letter-spacing: -0.4px;
      text-align: left;
      color: #fff;
    }

    .img-home {
      width: 417px;
      height: 400px;
      object-fit: contain;
    }
  }
}

.body {
  margin: auto;
  background-color: #fff;
  padding-top: 30px;
  padding-left: 4.2em;

  .m-bottom {
    padding-bottom: 40px;
  }

  .image {
    width: 139px;
  }

  .p-top {
    padding-top: 0px;
  }

  h1 {
    font-size: 35px;
    font-weight: bold;
    letter-spacing: -0.9px;
    text-align: left;
    color: #6c17b5;
    margin-bottom: 15px;
  }

  img {
    width: 139px;
    height: 139px;
  }

  h2 {
    font-size: 24px;
    font-weight: 500;
    letter-spacing: -0.6px;
    text-align: left;
    color: #000000;
  }

  small {
    font-size: 15px;
    letter-spacing: -0.4px;
    text-align: left;
    color: #263238;
  }

  .button {
    margin-top: 10px;
    display: block;
    width: 115px;
    height: 41px;
    border-radius: 100px;
    border: solid 2px #00cbff;
  }
}
</style>
