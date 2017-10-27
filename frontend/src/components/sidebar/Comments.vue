<template>
  <div class="comments-box">
    <div class="comments">

      <comment-item v-for="(data, index) in commentsList" :key="index" :comment="data"/>
    </div>

    <div class="form">
      <div class="columns is-marginless fields">
        <div class="column m-auto">
          <textarea name="" id="" cols="30" rows="10"></textarea>
        </div>

        <div class="column send is-2">
          <a href="">Send</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import CommentItem from './CommentsItem';

export default {
  name: 'Comments',

  components: { CommentItem },

  computed: {
    ...mapGetters({
      commentsList: 'getComments',
    }),
  },
};
</script>

<style lang="scss" scoped>
.comments-box {
  height: 90%;
  position: relative;

  .m-auto {
    margin: auto;
  }

  .comments {
    width: 100%;
		height: 86.7%;
		background-color:#cfcfcf;
    margin: 0 auto;
    overflow: auto;
    padding-top: 10px;
  }

  .form {
    width: 100%;
		height: 120px;
		background-color:#fff;
    margin: 0 auto;

    .fields {
      height: 100%;
    }

    textarea {
      width: 460px;
      height: 79px;
      border-radius: 16px;
      border: solid 2px #f0f0f0;
      outline: none;
      resize: none;
      padding-left: 7px;
    }
    
    .send {
      width: 95.5px;
      height: 51.7px;
      border-radius: 100px;
      border: solid 2px #00cbff;
      text-align: center;
      margin: auto;
      margin-right: 22px;
      background-color: #fff;

      a {
        margin: auto;
      }
    }
  }
}
</style>
