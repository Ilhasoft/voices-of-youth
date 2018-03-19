<template>
  <div 
    class="column is-paddingless profile-box" 
    @mouseover="isVisible = true" 
    @mouseout="isVisible = false">
    
    <div v-if="userIsLogged">
      <img class="avatar" :src="user.avatar" />

      <div class="profile-item" :class="[isVisible ? 'fade-in' : 'fade-out']">
        <div class="item">
          <div class="item-left">
            <img :src="user.avatar">
          </div>

          <div class="item-right">
            {{ user.first_name }}
            <small>{{ user.username }}</small>
          </div>
        </div>

        <div class="item">
          <div class="item-right">
            <router-link
              :to="{ name: 'profile' }">
              {{ $t('message.header.account.title') }}
            </router-link>
          </div>
        </div>

        <div class="item logout">
          <div class="item-right">
            <a href="" @click.prevent="logout()">
              {{ $t('message.header.account.logout') }}
            </a>
          </div>
        </div>
      </div>
    </div>

    <div v-else>
      <router-link
        :to="{ name: 'login' }"
        class="button btn-login">
        {{ $t('message.header.account.login') }}
      </router-link>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import router from '@/router';

export default {
  name: 'Account',

  data() {
    return {
      isVisible: false,
    };
  },

  computed: {
    ...mapGetters({
      userIsLogged: 'userIsLogged',
      user: 'getUserData',
      currentProject: 'getCurrentProject',
    }),
  },

  methods: {
    ...mapActions([
      'executeLogout',
    ]),

    logout() {
      this.executeLogout().then(() => {
        router.push({ name: 'project', params: { path: this.currentProject.path } });
      });
    },
  },
};
</script>

<style lang="scss" scoped>
.profile-box {
  height: 66px;
  margin: 5px 30px;
  z-index: 1;

  .avatar {
    width: 43px;
    height: 43px;
    cursor: pointer;
  }

  .btn-login {
    width: 112px;
    border-radius: 100px;
    border: solid 2px #00c9fd;
  }

  .profile-item {
    position: absolute;
    margin: 3px 10px 0px 0px;
    right: 0px;
    width: 223px;
    height: 166px;
    border-radius: 11px;
    background-color: #fff;
    box-shadow: 0 0 3px 0 rgba(0, 0, 0, 0.33);
    padding-top: 14px;

    .item {
      background-color: #fff;
      padding: 6px;

      .item-left {
        float: left;
        width: 30px;
        height: 30px;
        margin: 9px 0px 0px 10px;
      }

      .item-right {
        font-size: 18px;
        font-weight: 500;
        letter-spacing: -0.4px;
        text-align: left;
        margin-left: 50px;

        small {
          font-size: 14px;
          color: #9b9fa3;
          display: block;
        }
      }
    }

    .logout {
      border-top: solid 0.5px #cbcbcb;
      margin-left: 15px;
      margin-right: 15px;
      padding: 0px;

      .item-right {
        margin: 10px 40px;
      }
    }
  }
}
</style>
