<template>
  <div class="map-box">
    <div class="columns">
      <div class="column no-padding">
        <div class="columns header">
          <div class="column no-padding">
            <img src="../../assets/img/report-example-1.png" alt="">
          </div>
        </div>

        <div class="columns">
          <div class="column">
            <ul class="images">
              <li><img src="../../assets/img/report-example.png" alt=""></li>
              <li><img src="../../assets/img/report-example.png" alt=""></li>
              <li><img src="../../assets/img/report-example.png" alt=""></li>
              <li><img src="../../assets/img/report-example.png" alt=""></li>
              <li><img src="../../assets/img/report-example.png" alt=""></li>
              <li><img src="../../assets/img/report-example.png" alt=""></li>
              <li><img src="../../assets/img/report-example.png" alt=""></li>
              <li><img src="../../assets/img/report-example.png" alt=""></li>
              <li><img src="../../assets/img/report-example.png" alt=""></li>
              <li><img src="../../assets/img/report-example.png" alt=""></li>
            </ul>
          </div>
        </div>

        <div class="columns reports">
          <div class="column">
            <h1>Helps, but emission</h1>
            <small>Aug 02, 2016</small>

            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do consectetureiusmod tempor inciddipiscing elit, sed do dipLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do consectetureiusmod tempor inciddipiscing elit, sed do dipLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do consectetureiusmod tempor inciddipiscing elit, sed do dipLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do consectetureiusmod tempor inciddipiscing elit, sed do dip.ipiscing elit, sed do consectetureiusmod tempor inciddipiscing elit, sed do dipLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do </p>
          </div>
        </div>

        <div class="columns">
          <div class="column tags">
            <small>Accessibility</small>
            <small>Security</small>
            <small>Community</small>
          </div>
        </div>

        <div class="columns buttons">
          <div class="column">
            <a class="button share">
              <span class="icon-icon-share"></span> Share
            </a>
          </div>

          <div class="column">
            <a class="button share">
              <span class="icon-icon-comment"></span> Comment
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ReportDetail',
};
</script>

<style lang="scss" scoped>
.map-box {
  margin: auto;

  .no-padding {
    padding-right: 0px !important;
  }

  .buttons {
    margin-left: 7px;

    .share {
      width: 267.8px;
      height: 50px;
      border-radius: 10px;
      background-color: #ffffff;
      box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.3);

      font-size: 17px;
      text-align: left;
      color: #000000;

      span {
        font-size: 20px;
        margin-right: 5px;
      }
    }
  }

  .header {
    width: 100%;
    
    img {
      width: 100%;
      height: 200px;
    }
  }

  ul.images {
    width: 622px;
    margin: 0;
    padding: 0;
    white-space: nowrap;
    overflow-x: auto;
  }

  ul.images li {
    display: inline;
  }

  ul.images img {
    width: 86px;
    height: 86px;
    padding: 5px;
  }

  .reports {
    margin-left: 7px;

    h1 {
      font-size: 20px;
      font-weight: bold;
      letter-spacing: -0.5px;
      text-align: left;
      color: #9012fe;
    }

    small {
      font-size: 12px;
      text-align: left;
      color: #9012fe;
    }

    p {
      font-size: 14px;
      color: #000000;
      margin-top: 30px;
    }
  }

  .tags {
    margin-left: 18px;
    margin-right: 35px;

    small {
      margin-right: 3px;
      font-size: 13px;
      letter-spacing: -0.3px;
      text-align: center;
      color: #fff;
      padding: 5px;
      border-radius: 100px;
      background-color: #9012fe;
    }
  }

  h1 {
    font-size: 25px;
    font-weight: bold;
    letter-spacing: -0.6px;
    text-align: left;
    color: #ffffff;
  }
}
</style>
