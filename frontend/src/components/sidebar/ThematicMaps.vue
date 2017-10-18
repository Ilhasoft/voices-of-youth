<template>
  <div class="map-box">
    <div class="columns">
      <div class="column scrolling">
        <div class="columns is-mobile">
          <div class="column is-2 filter">
            <div class="field">
              <div class="control">
                <div class="select is-info">
                  <select>
                    <option>2017</option>
                    <option>2016</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          <div class="column is-1 m-auto">
            <p>to</p>
          </div>

          <div class="column is-2 filter">
            <div class="field">
              <div class="control">
                <div class="select is-info">
                  <select>
                    <option>2017</option>
                    <option>2016</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          <div class="column">
            <div class="control t-right">
              <label class="radio">
                Select all &nbsp;&nbsp;<checkbox-item />
              </label>
            </div>
          </div>
        </div>

        <div class="columns is-mobile item" :key="key" v-for="(value, key) in items">
          <div class="column is-1 m-auto center">
            <span class="icon-pin pin"></span>
          </div>

          <div class="column m-auto">
            <h1>Trash</h1>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do consectetureiusmod tempor inciddipiscing elit…See more</p>
          </div>

          <div class="column is-1 m-auto">
            <checkbox-item />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CheckboxItem from '../shared/Checkbox';

export default {
  name: 'ThematicMaps',

  components: { CheckboxItem },

  data() {
    return {
      items: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    };
  },
};
</script>

<style lang="scss" scoped>
.map-box {
  margin: auto;
  padding-left: 25px;

  .filter {
    width: 20% !important;
  }

  .t-right {
    text-align: right;
    margin-right: 12px;
  }

  .item {
    margin-top: 15px;
    margin-bottom: 15px;
    width: 100%;
    min-height: 125px;
    border-radius: 10px;
    background-color: #fff;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.16);
  }

  .scrolling {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    overflow-y: scroll;
    margin-top: 62px;
    margin-left: 20px;
  }

  .m-auto {
    margin: auto;
  }

  .pin {
    font-size: 38px;
    color: #9013fe;
  }

  .center {
    text-align: center;
  }

  h1 {
    font-size: 18px;
    font-weight: bold;
    letter-spacing: -0.5px;
    text-align: left;
    color: #000000;
  }

  p {
    font-size: 15px;
    line-height: 1.33;
    letter-spacing: -0.4px;
    text-align: left;
    color: #000000;
  }
}
</style>
