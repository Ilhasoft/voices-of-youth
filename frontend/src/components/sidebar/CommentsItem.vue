<template>
  <div class="columns item">
    <div class="column is-1">
      <img v-if="comment.created_by.avatar" :src="comment.created_by.avatar" alt=""/>
    </div>

    <div class="column text">
      <h1>{{ comment.created_by.first_name }}</h1>
      <small>Aug 03, 2017</small>
      <p>{{ comment.text }}</p>
    </div>

    <div class="column is-1 t-center" @mouseover="isVisible = true" @mouseout="isVisible = false">
      <span class="icon-icon-more more"></span>
      <div class="actions" :class="[isVisible ? 'fade-in' : 'fade-out']">
        <p><a>Edit</a></p>
        <p><a>Remove</a></p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CommentItem',

  props: {
    comment: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      isVisible: false,
    };
  },

  methods: {
    formatDate() {
      const date = new Date(this.comment.created_on);
      return `${date.toLocaleString('en-use', { month: 'short' })} ${date.getDay()}, ${date.getFullYear()}`;
    },
  },
};
</script>

<style lang="scss" scoped>
.item {
  background: #efefef;
  padding-left: 25px;
  margin-right: 0px;
  border-bottom: solid 0.5px #979797;

  img {
    margin-top: 15px;
  }

  .more {
    font-size: 24px;
    z-index: 10;
  }

  .actions {
    width: 83px;
    height: 79px;
    border-radius: 5px;
    background-color: #fff;
    box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.14);
    text-align: left;
    position: relative;

    margin-top: -34px;
    margin-left: -55px;

    p {
      margin-left: 15px;
      padding-top: 10px;
    }

    a {
      font-size: 14px;
      letter-spacing: -0.3px;
      text-align: center;
      color: #4a4a4a;
    }
  }

  .text {
    h1 {
      font-size: 16px;
      font-weight: 500;
    }

    small {
      font-size: 12px;
    }

    p {
      margin-top: 15px;
      font-size: 12px;
      text-align: left;
    }
  }

  .t-center {
    text-align: center;
    cursor: pointer;
  }
}
</style>
