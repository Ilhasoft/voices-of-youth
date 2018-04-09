<template>
  <div class="columns item">
    <div class="column is-3">
      <img :src="report.thumbnail" alt="" v-if="report.thumbnail">
    </div>

    <div class="column text">
      <h4 class="is-marginless">{{ report.name }}</h4>
      <small>{{ formatDate() }}</small>
      <p>{{ report.description }}</p>
      <p v-show="report.last_notification">{{ $t('message.pages.myreports.report.admin') }}: <i>{{ report.last_notification }}</i></p>
    </div>

    <div class="column is-2 m-auto">
      <button
        class="button btn-edit"
        @click.prevent="openReport(report)"
        v-if="report.status == 1">
        {{ $t('message.pages.myreports.report.btnView') }}
      </button>

      <button
        class="button btn-edit"
        @click.prevent="editReport"
        v-if="report.status == 2 || report.status == 3">
        {{ $t('message.pages.myreports.report.btnEdit') }}
      </button>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import helper from '@/helper';
import router from '@/router/';

export default {
  name: 'ReportItem',

  props: {
    report: {
      type: Object,
      required: true,
    },
  },

  computed: mapGetters({
    currentProject: 'getCurrentProject',
  }),

  methods: {
    ...mapActions([
      'setSideBarConfigs',
      'getReport',
    ]),

    formatDate() {
      return helper.formatDate(this.report.created_on);
    },

    editReport() {
      router.push({ name: 'editreport', params: { path: this.currentProject.path, id: this.report.id } });
    },

    openReport(item) {
      router.replace({ name: 'project', params: { path: this.currentProject.path } });
      this.setSideBarConfigs({
        tabActived: 'ReportDetail',
        isActived: true,
      }).then(() => {
        this.getReport(item.id);
      });
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
