<template>
  <div class="empty">
    <div class="columns">
      <div class="column">
        <img src="~@/assets/img/my-report-approved.png" alt="" v-show="status === 'approved'" />
        <img src="~@/assets/img/my-report-pending.png" alt="" v-show="status === 'pending'" />
        <img src="~@/assets/img/my-report-rejected.png" alt="" v-show="status === 'rejected'" />
      </div>
    </div>

    <div class="columns">
      <div class="column">
        <h1>{{ text }}</h1>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EmptyList',

  props: {
    text: {
      type: String,
      required: true,
      default: '',
    },

    status: {
      type: String,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped>
.empty {
  margin-top: 50px;

  h1 {
    font-size: 25px;
    font-weight: bold;
    text-align: center;
    color: #4a4a4a;
  }
}
</style>
