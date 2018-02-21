<template>
  <div>
    <header-index/>
    <div class="internal-page-color">
      <div class="container">
        <div class="columns t-center m-top">
          <div class="column content-report">
            <div class="columns">
              <div class="column is-4">
                <button class="button" :class="[status == 'approved' ? 'btn' : 'btn-clear']" @click.prevent="getReports('approved', '1')">Approved</button>
              </div>

              <div class="column is-4">
                <button class="button" :class="[status == 'pending' ? 'btn' : 'btn-clear']" @click.prevent="getReports('pending', '2')">Pending</button>
              </div>

              <div class="column is-4">
                <button class="button" :class="[status == 'rejected' ? 'btn' : 'btn-clear']" @click.prevent="getReports('rejected', '3')">Not Approved</button>
              </div>
            </div>

            <report-item
              :key="key"
              :report="report"
              v-for="(report, key) in reports" />
            
            <empty-list
              :avatar="user.avatar"
              :text="text"
              v-show="isEmpty" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import router from '@/router/';
import HeaderIndex from '@/components/header/Index';
import ReportItem from '@/components/my-reports/Report';
import EmptyList from '@/components/my-reports/Empty';

export default {
  name: 'MyReports',

  components: { HeaderIndex, ReportItem, EmptyList },

  data() {
    return {
      status: '',
      text: '',
      isEmpty: false,
      descriptions: {
        approved: 'Ups! You have not created any reports yet',
        pending: 'Great! All your reports have been approved',
        rejected: 'Good job! You have no unapproved reports',
      },
    };
  },

  beforeCreate: () => {
    document.body.className = 'grey';
  },

  beforeDestroy: () => {
    document.body.className = 'white';
  },

  mounted() {
    if (!this.userIsLogged || !this.userIsMapper) {
      router.push({ name: 'project', params: { path: this.currentProject.path } });
    } else {
      this.getReports('approved', 1);
    }
  },

  computed: mapGetters({
    reports: 'getMyReports',
    userIsLogged: 'userIsLogged',
    userIsMapper: 'userIsMapper',
    currentProject: 'getCurrentProject',
    user: 'getUserData',
  }),

  methods: {
    ...mapActions([
      'myReports',
    ]),

    getReports(status, type) {
      this.status = status;
      this.myReports(type).then((response) => {
        if (response.length === 0) {
          this.text = this.descriptions[status];
          this.isEmpty = true;
        } else {
          this.isEmpty = false;
        }
      });
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

.container {
  height: 100vh;
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
    background: url('~@/assets/img/header-search.png') #ffffff no-repeat;
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
