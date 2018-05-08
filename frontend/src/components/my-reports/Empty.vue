<template>
  <div class="empty">
    <div class="columns">
      <div class="column">
        <img :src="avatar" alt="" />
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

    avatar: {
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
    font-weight: 500;
    text-align: center;
    color: #4a4a4a;
  }
}
</style>
