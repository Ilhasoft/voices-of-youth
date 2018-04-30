<template>
  <div>
    <div class="header">
      <div class="logo">
        <img src="~@/assets/img/logo-home.png" alt="">
      </div>

      <div class="slide">
        <img src="~@/assets/img/slide-home.png" alt="">
      </div>
    </div>

    <div class="container">
      <div class="columns is-marginless">
        <div class="column is-5 is-offset-1 about">
          <img src="~@/assets/img/img_about.png" alt="">

          <div class="columns">
            <div class="column">
              <h4>About The Project</h4>
            </div>
          </div>

          <div class="columns">
            <div class="column">
              <p>Voices of Youth offers inspiring, original insight and opinion from across the globe – from young people, for young people. Did you ever ask yourself, where are all the young people who actually do give a damn? Well, they’re right here. Countering disheartening headlines about today’s young generation, the Voices of Youth community proves that young people ARE making a difference, each and every day. But making a difference doesn’t have to be boring – we bring you fresh and honest views and stories, written and filmed by our unbeatable international youth bloggers. Want to be part of our pool of youth bloggers? Do it! Anybody is welcome to write, film, comment and engage in discussions – let’s go!</p>
            </div>
          </div>
        </div>

        <div class="column is-4 is-offset-1 is-mobile">
          <div class="digital-mapper">
            <div class="columns is-mobile">
              <div class="column is-3">
                <img src="~@/assets/img/avatar-home.png" alt="">
              </div>
              <div class="column">
                <h2>I’m a digital mapper</h2>
                <p>Log into your map to start mapping:</p>
              </div>
            </div>

            <div class="columns">
              <div class="column">
                <select name="" id="" class="select"></select>
              </div>
            </div>

            <div class="columns">
              <div class="column has-text-right">
                <button class="button">Enter</button>
              </div>
            </div>
          </div>

          <div class="columns is-mobile feature">
            <div class="column">
              <div class="columns is-mobile">
                <div class="column is-2">
                  <img src="~@/assets/img/home-group.png" alt="">
                </div>
                <div class="column m-auto no-pad-l">
                  <h4>Featured Reports</h4>
                </div>
              </div>

              <div class="columns">
                <div class="column">
                  <div class="report" v-for="item in items" :key="item">
                    <div class="columns is-gapless is-mobile">
                      <div class="column is-3">
                        <img src="~@/assets/img/home-report.png" alt="">
                      </div>
                      <div class="column text">
                        <h1>Trash in the streets</h1>
                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor ut labore et dolore magna aliqua.</p>
                      </div>
                    </div>
                  </div>
                  <div class="has-text-right">
                    <a href="">See all</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="columns is-12 is-marginless">
        <div class="column is-offset-1 explore">
          <h1>Explore where young<br/>people are mapping</h1>
        </div>
      </div>
    </div>
    
    
    
      <!-- <div class="header-info container">
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
      </div> -->
    

    <!-- <div class="body container">
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
    </div> -->
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import router from '@/router/';

export default {
  name: 'Home',

  data() {
    return {
      items: [1, 2, 3],
    };
  },

  mounted() {
    this.setProjects();
    window.localStorage.clear();
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
@import url('https://fonts.googleapis.com/css?family=Roboto');

.header {
  width: 100%;
  margin: 0px;

  .logo {
    background-color: #009ee3;
    padding-top: 9px;
    padding-bottom: 9px;
    height: 49px;

    img {
      margin-left: 18%;
      position: absolute;
    }

    @media (max-width: 990px) {
      img {
        margin-left: 45%;
      }
    }
  }
}

.slide {
  text-align: center;

  img {
    height: 426px !important;
  }  
}

.container {
  padding: 30px 100px 0 100px;

  @media (max-width: 990px) {
    padding: 30px 0px 0px 0px;
  }

  .m-auto {
    margin: auto;
  }

  .about {
    color: #000000;
    text-align: left;
    font-family: 'Roboto';

    h4 {  
      font-size: 40px;
      font-weight: bold;
    }

    p {
      font-size: 14px;
    }
  }

  .no-pad-l {
    padding-left: 0px;
  }

  .digital-mapper {
    min-height: 226px;
    background-color: #009ee3;
    border-radius: 8px;
    color: #ffffff;
    font-family: 'Roboto';
    text-align: left;
    padding: 20px;

    .select {
      height: 50px;
      width: 100%;
      background-color: #ffffff;
      border-radius: 8px;
    }

    .pr-70 {
      padding-right: 72px;
    }

    .button {
      height: 41px;
      width: 125px;
      background-color: #0077ac;
      border-radius: 8px;
      border-color: #0077ac;
      font-family: 'Roboto';
      font-size: 14px;
      font-weight: 500;
      color: #ffffff;
      text-align: center;
    }

    h2 {
      font-size: 20px;
      font-weight: 500;
    }

    p {
      font-size: 14px;
    }
  }

  .feature {
    margin-top: 21px;
    font-family: 'Roboto';

    h4 {
      font-size: 24px;
      font-weight: 500;
      color: #000000;
      text-align: left;
    }

    a {
      color: #4a90e2;
      font-size: 18px;
      color: #4a90e2;
      text-align: right;
    }

    .report {
      margin-bottom: 10px;
      background-color: #ffffff;
      border: 1px solid #c3c3c3;
      border-radius: 8px;
      padding: 15px;

      .text {
        padding-left: 12px !important;
      }

      h1 {
        font-size: 20px;
        font-weight: 500;
        color: #000000;
        text-align: left;
      }

      p {
        font-size: 12px;
        color: #000000;
      }
    }
  }

  .explore {
    font-size: 40px;
    font-weight: bold;
    color: #000000;
    text-align: left;
  }
}

  // .m-auto {
  //   margin: auto;
  // }

  // .header-info {
  //   margin: auto;
  //   background-color: #00cbff;

  //   h1 {
  //     line-height: normal;
  //     font-size: 50px;
  //     font-weight: bold;
  //     letter-spacing: -1.3px;
  //     text-align: left;
  //     color: #fff;
  //   }

  //   small {
  //     font-size: 25px;
  //     letter-spacing: -0.6px;
  //     text-align: left;
  //     color: #fff;
  //   }

  //   p {
  //     margin-top: 25px;
  //     font-size: 15px;
  //     line-height: 1.67;
  //     letter-spacing: -0.4px;
  //     text-align: left;
  //     color: #fff;
  //   }

  //   .img-home {
  //     width: 417px;
  //     height: 400px;
  //     object-fit: contain;
  //   }
  // }

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
