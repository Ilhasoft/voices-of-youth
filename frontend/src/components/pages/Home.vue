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
      <div class="slide">
        <carousel :per-page="1" paginationColor="#009ee3" :mouse-drag="true">
          <slide v-for="(image, key) in images" :key="key">
            <img :src="image.thumbnail" alt="">
          </slide>
        </carousel>
      </div>

      <div class="columns is-marginless">
        <div class="column is-4 is-offset-1 about">
          <img :src="about.thumbnail" class="is-hidden-mobile" alt="">

          <div class="columns">
            <div class="column">
              <h4>About The Project</h4>
            </div>
          </div>

          <div class="columns">
            <div class="column">
              <p v-html="about.project"></p>
            </div>
          </div>
        </div>

        <div class="column is-4 is-offset-2 is-mobile">
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
                <div class="column is-2 is-hidden-mobile">
                  <img src="~@/assets/img/home-group.png" alt="">
                </div>
                <div class="column m-auto">
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
                    <router-link
                      :to="{ name: 'reports' }">
                      See all
                    </router-link>
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

      <div class="projects">
        <div class="columns is-marginless is-hidden-touch" v-for="item in [0, 1]" :key="item">
          <div class="column is-10 is-offset-1">
            <div class="columns">
              <div class="column" v-for="item in items" :key="item">
                <div class="is-paddingless box">
                  <img src="~@/assets/img/report-example-1.png" alt="">
                  <div class="text">
                    <h4>Mongólia</h4>
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="is-hidden-desktop">
          <div>
            <div class="columns is-marginless is-mobile is-variable is-1 scroll">
              <div class="column is-5" v-for="(project, key) in projectsToMobile" :key="key">
                <div class="is-paddingless box">
                  <img :src="project.thumbnail_home_responsive" v-if="project.thumbnail_home_responsive" alt="">
                  <div class="text">
                    <h4>{{ project.name }}</h4>
                    <p>{{ project.description }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="has-text-centered see-all">
          <router-link
            :to="{ name: 'projects' }">
            See all
          </router-link>
        </div>
      </div>
    </div>

    <div class="columns is-marginless about-voy">
      <div class="column is-half is-offset-one-quarter">
        <div class="text">
          <h1>Voices of youth</h1>
          <p>{{ about.voy }}</p>
        </div>
      </div>
    </div>

    <div class="footer">
      <div class="columns is-marginless">
        <div class="column is-4 is-offset-2">
          <h4>Join us</h4>
          <p>If you wish to become a mapper, fill out the form and we will get back to you</p>

          <form action="" class="form">
            <p>
              <input type="text" name="" placeholder="Name" />
            </p>
            <p>
              <input type="email" name="" placeholder="Email" />
            </p>
            <p>
              <select name="" id="" class="select">
                <option value="">What do you want?</option>
                <option value="">I wanna be a mapper?</option>
                <option value="">Questions or suggestions</option>
              </select>
            </p>
            <p>
              <select name="" id="" class="select">
                <option value="">Choose a project?</option>
              </select>
            </p>
            <p>
              <textarea name="" id="" cols="30" rows="10"></textarea>
            </p>
            <div class="columns buttons">
              <div class="column">
                <div class="columns">
                  <div class="column">
                    <vue-recaptcha class="g-recaptcha" sitekey="6Lcp41YUAAAAAGNhDzBMW2ZzO33JJ6LdAY_aeE9g" />
                  </div>
                </div>
                <div class="columns">
                  <div class="column is-4 btn-submit">
                    <button class="submit">Send</button>
                  </div>
                </div>
              </div>
            </div>
          </form>
        </div>

        <div class="column is-offset-1">
          <!-- <iframe src="https://www.facebook.com/plugins/page.php?href=https%3A%2F%2Fwww.facebook.com%2Fvoicesofyouth&tabs=timeline&width=340&height=500&small_header=false&adapt_container_width=true&hide_cover=true&show_facepile=true&appId" width="340" height="500" style="border:none;overflow:hidden" scrolling="no" frameborder="0" allowTransparency="true" allow="encrypted-media"></iframe> -->
        </div>
      </div>

      <div class="columns terms">
        <div class="column">
          <p class="has-text-centered">Privacy policy and terms of use</p>
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
import VueRecaptcha from 'vue-recaptcha';
import { Carousel, Slide } from 'vue-carousel';
import router from '@/router/';

export default {
  name: 'Home',

  components: { VueRecaptcha, Carousel, Slide },

  data() {
    return {
      items: [1, 2, 3],
      images: [],
      projects: [],
      projectsToMobile: [],
      about: {
        thumbnail: null,
        project: '',
        voy: '',
      },
    };
  },

  mounted() {
    // this.setProjects();
    this.getHomeSlide().then((images) => {
      this.images = images;
    });

    this.getAboutProject().then((about) => {
      this.about.thumbnail = about.thumbnail;
      this.about.project = about.about_project.replace('\n', '<br/>');
      this.about.voy = about.about_voy;
    });

    this.getProjects().then((projects) => {
      // this.projects = projects;
      this.projects = this.chunck(projects, 3);
      this.projectsToMobile = projects;
    });
  },

  computed: {
    ...mapGetters({
      projectsList: 'getAllProjects',
    }),
  },

  methods: {
    ...mapActions([
      // 'setProjects',
      'setCurrentProject',
      'showDisclaimerProject',
      'getHomeSlide',
      'getAboutProject',
      'getProjects',
    ]),

    openProject(item) {
      this.setCurrentProject(item).then(() => {
        router.push({ name: 'project', params: { path: item.path } });
        this.showDisclaimerProject(true);
      });
    },

    chunck(r, j) {
      /* eslint-disable no-confusing-arrow */
      const array = r.reduce((a, b, i, g) => !(i % j) ? a.concat([g.slice(i, i + j)]) : a, []);
      return array;
    },
  },

  beforeCreate: () => {
    document.body.className = 'home';
  },
};
</script>

<style lang="scss" scoped>
@import url('https://fonts.googleapis.com/css?family=Roboto:400,500');

.header {
  background-color: #009ee3;
  width: 100%;
}

.slide {
  text-align: center;
}

.scroll {
  overflow-y: scroll;
}

.container {
  font-weight: 400;

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

  .projects {
    .box {
      border: 1px solid #c3c3c3;
      border-radius: 8px;

      .text {
        font-family: 'Roboto';
        color: #000000;
        text-align: left;
        padding: 18px;

        h4 {
          font-size: 18px;
          font-weight: 500;
        }

        p {
          margin-top: 36px;
          font-size: 14px;
        }
      }

      @media (max-width: 495px) {
        .text {
          padding: 0px 8px 8px 8px;

          h4 {
            font-size: 14px;
            font-weight: 500;
          }
  
          p {
            width: 9rem;
            margin-top: 0px;
            font-size: 12px;
          }
        }
      }

      img {
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        width: 100%;
      }
    }

    .see-all {
      margin-top: 31px;
      margin-bottom: 40px;

      a {
        font-size: 18px;
        color: #4a90e2;
      }
    }
  }
}

.about-voy {
  color: #ffffff;
  text-align: left;
  background-image: url('~@/assets/img/home-bg-footer.png');
  background-size: cover;
  background-position: bottom;
  width: 100%;
  height: 305px;

  .text {
    margin: auto;
    width: 26rem;
    word-wrap: break-word;

    h1 {
      margin-top: 57px;
      font-size: 55px;
      font-weight: bold;
    }

    p {
      font-size: 16px;
    }
  }

  @media (max-width: 495px) {
    .text {
      h1 {
        font-size: 42px;
      }

      width: 19rem;
    }
  }
}

.footer {
  background-color: #009ee3;
  color: #ffffff;
  text-align: left;
  padding-bottom: 0px;

  h4 {
    font-size: 40px;
    font-weight: bold;  
  }

  p {
    font-size: 16px;
  }

  .form {
    margin-top: 40px;

    input, select, textarea {
      margin: 10px 0px 10px 0px;
      background-color: #ffffff;
      outline: none;
      border: none;
    }

    input[type='text'], input[type='email'] {
      border-radius: 4px;
      height: 37px;
      width: 100%;
      padding-left: 5px;
      font-size: 18px;
      color: #7b7b7b;
    }

    .select {
      height: 37px;
      width: 100%;
      
      border-radius: 8px;
      font-size: 18px;
      color: #7b7b7b;
    }

    textarea {
      height: 83px;
      width: 100%;
      border-radius: 4px;
      padding: 5px;
      resize: none;
      font-size: 18px;
      color: #7b7b7b;
    }

    .buttons {
      margin-top: 40px;

      .btn-submit {
        text-align: right;

        button {
          height: 50px;
          width: 100%;
          background-color: #0379ac;
          border-radius: 8px;
          border: none;
          font-family: 'Roboto';
          font-size: 16px;
          font-weight: bold;
          color: #ffffff;
        }
      }
    }
  }

  .terms {
    margin-top: 145px;
  }
}
</style>
