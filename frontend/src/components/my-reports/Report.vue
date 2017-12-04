<template>
  <div class="columns item">
    <div class="column is-3">
      <img :src="report.last_image.file" alt="" v-if="report.last_image">
    </div>

    <div class="column text">
      <h4 class="is-marginless">{{ report.name }}</h4>
      <small>{{ formatDate() }}</small>
      <p>{{ report.description }}</p>
    </div>

    <div class="column is-2 m-auto">
      <!-- <button class="button btn-edit">Edit</button> -->
    </div>
  </div>
</template>

<script>
import helper from '../../helper';

export default {
  name: 'ReportItem',

  props: {
    report: {
      type: Object,
      required: true,
    },
  },

  methods: {
    formatDate() {
      return helper.formatDate(this.report.created_on);
    },
  },
};
</script>

<style lang="scss" scoped>
.item {
  margin-top: 15px;
  border-radius: 10px;
  background-color: #fff;

  .m-auto {
    margin: auto;
  }

  img {
    max-width: 190px;
    max-height: 153px;
    object-fit: contain;
  }

  .p-left {
    padding-left: 0px;
  }

  .btn-edit {
    width: 63px;
    height: 35px;
    border-radius: 47px;
    background-color: #7ed321;
    font-size: 16px;
    font-weight: 500;
    letter-spacing: -0.4px;
    text-align: center;
    color: #ffffff;
  }

  .text {
    text-align: justify;
    letter-spacing: -0.5px;
    color: #000000;

    h4 {
      font-size: 20px;
      font-weight: 500;  
    }

    small {
      font-size: 14px;
      letter-spacing: -0.4px;
    }

    p {
      margin-top: 15px;
      font-size: 14px;
      letter-spacing: -0.3px;
    }
  }

  .btn-edit:focus {
    border-color: #7ed321;
    -webkit-box-shadow: none;
    box-shadow: none;
  }
}
</style>
