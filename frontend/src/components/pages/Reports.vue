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
            <a href="">Home</a>&nbsp;&gt;&nbsp;All Featured Reports
          </div>
          <h4>All Featured Reports</h4>
          <div class="columns">
            <div class="column is-10 projects">
              <div class="project" v-for="item in [0, 1, 2, 3]" :key="item">
                <div class="columns">
                  <div class="column">
                    <div class="columns is-mobile">
                      <div class="column is-2">
                        <img src="~@/assets/img/home-report.png" alt="">
                      </div>
                      <div class="column no-pad-l text">
                        <h1>Chili</h1>
                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod temporut labore et dolore magna aliqua.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod temporut labore et dolore magna aliqua.</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="has-text-centered show-more">
                <a href="">Show more</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
  </div>
</template>

<script>
export default {
  name: 'Projects',
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
