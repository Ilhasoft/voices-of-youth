<template>
  <div>
    <header-index/>
    <div class="container block">
      <div class="tile is-ancestor">
        <div class="tile is-parent">
          <article class="tile is-child">
            <div class="content">
              <div class="columns">
                <div class="column has-text-center">
                  <img :src="user.avatar" alt="">
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-center">
                  <h1>Hello, {{ user.first_name }}</h1>
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-center">
                  <input type="text" class="input" v-model="name" />
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-center">
                  <input type="email" class="input" name="name" v-model="email"/>
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-center">
                  <h2>Change password</h2>
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-center">
                  <input type="password" class="input" v-model="password" placeholder="New password"/>
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-center">
                  <input type="password" class="input" v-model="confirmPassword" placeholder="Confirm password"/>
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-right-desktop">
                  <button type="submit" @click.prevent="update" class="btn button l-submit">Save</button>
                </div>
              </div>
            </div>
          </article>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import HeaderIndex from '../header/Index';

export default {
  name: 'Login',

  data() {
    return {
      name: '',
      email: '',
      password: '',
      confirmPassword: '',
    };
  },

  components: { HeaderIndex },

  computed: {
    ...mapGetters({
      user: 'getUserData',
    }),
  },

  mounted() {
    this.name = this.user.first_name;
    this.email = this.user.email;
  },

  methods: {
    ...mapActions([
      'executeUpdateProfile',
      'executeUpdatePassword',
      'notifyOpen',
    ]),

    updateProfile() {
      if (this.name) {
        this.executeUpdateProfile({
          name: this.name,
          email: this.email,
        });
      }
    },

    update() {
      if (this.password && this.confirmPassword && this.password === this.confirmPassword) {
        this.executeUpdatePassword(this.password);
        this.updateProfile();
      } else {
        this.updateProfile();
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.btn {
  outline: none;
  font-size: 18px;
  font-weight: 500;
  letter-spacing: -0.4px;
  text-align: center;
  color: #4a4a4a;
  background-color: #fff;
  min-width: 189px;
  height: 51px;
  border-radius: 100px;
}

.block {
  margin-top: 30px;

  .content {
    margin: auto;
    max-width: 416px;
  }

  img {
    width: 77px;
    height: 77px;
  }

  .has-text-center {
    text-align: center;
  }

  h1 {
    font-size: 30px;
    font-weight: 500;
    letter-spacing: -0.8px;
    text-align: center;
    color: #9012fe;
  }

  h2 {
    font-size: 20px;
    letter-spacing: -0.5px;
  }

  .input {
    height: 59px;
    border-radius: 100px;
    background-color: #ffffff;
    border: solid 2px #e9e9e9;
    outline: none;
    font-size: 15px;
    letter-spacing: -0.4px;
    color: #4a4a4a;
    padding-left: 26px;
  }

  .input:focus {
    border-color: #e9e9e9;
    -webkit-box-shadow: none;
    box-shadow: none;
  }

  .l-submit {
    border: solid 2px #7ed321;
  }
}
</style>
