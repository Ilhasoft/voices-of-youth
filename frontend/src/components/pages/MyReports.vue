<template>
  <div>
    <header-index/>
    <div class="internal-page-color">
      <div class="container">
        <div class="columns t-center m-top">
          <div class="column content-report">
            
          <div class="columns">
            <div class="column is-2">
              <button class="button" :class="[status == 'approved' ? 'btn' : 'btn-clear']" @click.prevent="setStatus('approved', 'Ups! You have not created any report yet')">Approved</button>
            </div>
            <div class="column is-2">
              <button class="button" :class="[status == 'pending' ? 'btn' : 'btn-clear']" @click.prevent="setStatus('pending', 'Great! All your reports has been approved')">Pending</button>
            </div>
            <div class="column is-2">
              <button class="button" :class="[status == 'rejected' ? 'btn' : 'btn-clear']" @click.prevent="setStatus('rejected', 'Good job! You have no rejected reports')">Rejected</button>
            </div>
            <div class="column">
              <input type="text" class="input" placeholder="Search for report" />
            </div>
          </div>

          <report-item v-show="status == ''" />
          <report-item v-show="status == ''" />

          <empty-list :status="status" :text="textTag" v-show="status" />

          <div class="columns" v-show="status == ''">
            <div class="column">
              <p class="more-oldest"><a href="">More oldest</a></p>
            </div>
          </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import HeaderIndex from '../header/Index';
import ReportItem from '../my-reports/Report';
import EmptyList from '../my-reports/Empty';

export default {
  name: 'MyReports',

  components: { HeaderIndex, ReportItem, EmptyList },

  data() {
    return {
      status: '',
      textTag: '',
    };
  },

  beforeCreate: () => {
    document.body.className = 'grey';
  },

  beforeDestroy: () => {
    document.body.className = 'white';
  },

  methods: {
    setStatus(status, text) {
      this.status = status;
      this.textTag = text;
    },
  },
};
</script>

<style lang="scss" scoped>
.t-center {
  text-align: center;
}

.m-top {
  margin-top: 15px;
}

.content-report {
  margin: auto;
  max-width: 800px;

  .more-oldest {
    border-top: solid 1px #d2d2d2;
    padding-top: 10px;

    a {
      margin-top: 5px;
      font-size: 16px;
      letter-spacing: -0.4px;
      color: #00cbff;
    }
  }

  .btn {
    border-radius: 100px;
    background-color: #00cbff;
    font-size: 15px;
    letter-spacing: -0.4px;
    text-align: center;
    color: #ffffff;
    border-color: #00cbff;
    outline: none;
  }

  .btn:focus {
    border-color: #00cbff;
    -webkit-box-shadow: 0 0 0 0.125em rgba(0,203,255, 0.2);
    box-shadow: 0 0 0 0.125em rgba(0,203,255, 0.2);
  }

  .btn-clear {
    background-color: #f6f6f6;
    border-color: #f6f6f6;
  }

  .btn-clear:focus {
    border-color: #f6f6f6;
    -webkit-box-shadow: 0 0 0 0.125em rgba(246, 246, 246, 0.2);
    box-shadow: #f6f6f6;
  }

  .input {
    width: 326px;
    height: 38px;
    border-radius: 21px;
    border: solid 1px #e9e9e9;
    background: url('../../assets/img/header-search.png') #ffffff no-repeat;
    background-position: right 15px top 7px;
    padding-right: 42px;
  }

  .input:focus {
    border-color: #e9e9e9;
    -webkit-box-shadow: none;
    box-shadow: none;
  }
}
</style>
