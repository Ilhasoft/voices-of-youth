<template>
  <div v-show="isVisibled">
    <div class="opacity"></div>
    <div class="intro">
      <div class="header">
        <img src="./../../assets/img/intro.png"/>
      </div>
      <div class="body">
        <h3>Welcome to UNICEF's Youth Led Digital Mapping in Rio de Janeiro, Brazil</h3>

        <p>This project explores tools to help youth build impactful, communicative digital maps using mobile and web technologies. A phone application allows youth to produce a portrait of their community through geo-located photos and videos, organized in thematic maps.</p>

        <div class="join">
          <a class="button btn-join" @click.prevent="dismissIntro">Let's go!</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'IntroProject',

  data() {
    return {
      isVisibled: true,
    };
  },

  methods: {
    dismissIntro() {
      this.isVisibled = false;
    },
  },
};
</script>

<style lang="scss" scoped>
.opacity {
  opacity: 0.33;
  z-index: 1;
  background-color: #000000;
  width: 100%;
  height: 100%;
  position: fixed;
  left: 0;
  top: 0;
}

.intro {
  z-index: 10;
  position: relative;
  margin: auto;
  width: 553px;
  height: 708px;

  .header {
    width: 100%;
    height: 249px;
    background-color: #00cbff;
    border-top-left-radius: 30px;
    border-top-right-radius: 30px;
    display: table-cell; 
    vertical-align: middle; 
    text-align: center;
    width: inherit;
  }

  .body {
    width: 100%;
    height: 459px;
    background-color: #fff;
    border-bottom-left-radius: 30px;
    border-bottom-right-radius: 30px;
    padding: 41px;

    h3 {
      font-size: 32px;
      font-weight: bold;
      letter-spacing: -0.8px;
      text-align: left;
      color: #7412fe;
    }

    p {
      margin-top: 36px;
      font-size: 15px;
      line-height: 1.67;
      letter-spacing: -0.4px;
      text-align: left;
      color: #000000;
      min-height: 110px;
    }

    .join {
      text-align: center;
      margin-top: 15px;

      .btn-join {
        width: 164px;
        height: 49px;
        border-radius: 100px;
        background-color: #6f18bb;
        
        font-size: 17px;
        font-weight: 500;
        letter-spacing: -0.4px;
        color: #ffffff;
      }
    }
  }
}
</style>
