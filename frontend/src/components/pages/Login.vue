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
                  <img src="./../../assets/img/login-a.png" alt="">
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-center">
                  <h1>Hello, again!</h1>
                  <small>Login to your account</small>
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-center">
                  <input type="text" class="input" name="name" value="" placeholder="Name" v-model="login.username"/>
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-center">
                  <input type="password" class="input" name="password" placeholder="Password" v-model="login.password"/>
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-center">
                  <a href="" class="forgot">Forgot password?</a>
                </div>

                <div class="column has-text-center">
                  <button type="submit" @click.prevent="execLogin()" class="btn button l-submit">Login</button>
                </div>
              </div>
            </div>
          </article>
        </div>

        <div class="tile is-parent">
          <article class="tile is-child">
            <div class="content">
              <div class="columns">
                <div class="column has-text-center">
                  <img src="./../../assets/img/login-b.png" alt="">
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-center">
                  <h1>I'm new here</h1>
                  <small>Create a new account</small>
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-center">
                  <input type="text" class="input" name="name" value="" placeholder="Full name"/>
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-center">
                  <input type="text" class="input" name="name" value="" placeholder="E-mail"/>
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-center">
                  <input type="password" class="input" name="name" value="" placeholder="Password"/>
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-center">
                  <input type="password" class="input" name="name" value="" placeholder="Confirm password"/>
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-center">
                  <label class="checkbox">
                    <input type="checkbox" @change.prevent="openTerms" v-model="isAccepted">
                    Terms and conditions
                  </label>
                </div>

                <div class="column has-text-center">
                  <button type="submit" class="btn button l-register">Register</button>
                </div>
              </div>
            </div>
          </article>
        </div>
      </div>
    </div>

    <div v-show="isOpened">
      <div class="opacity"></div>
      <div class="terms">
        <div class="columns">
          <div class="column">
            <img src="./../../assets/img/logo.png" class="logo" alt="">
          </div>
        </div>

        <div class="columns">
          <div class="column is-paddingless">
            <h1>Terms and Conditions</h1>
          </div>
        </div>

        <div class="columns">
          <div class="column">
            <div class="terms-text">
              <p>"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
              <br/>
              <p>"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
              <br/>
              <p>"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
              <br/>
              <p>"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
              <br/>
              <p>"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
              <br/>
              <p>"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
            </div>
          </div>
        </div>

        <div class="columns">
          <div class="column has-text-center">
            <button class="btn button l-refuse" @click.prevent="closeTerms(false)">Refuse</button>
          </div>

          <div class="column has-text-center">
            <button class="btn button l-accept" @click.prevent="closeTerms(true)">Accept</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import HeaderIndex from '../header/Index';

export default {
  name: 'Login',

  components: { HeaderIndex },

  data() {
    return {
      isOpened: false,
      isAccepted: false,

      login: {
        username: '',
        password: '',
      },
    };
  },

  methods: {
    ...mapActions([
      'executeLogin',
    ]),

    openTerms() {
      this.isOpened = !this.isOpened;
    },

    closeTerms(value) {
      this.isOpened = false;
      this.isAccepted = value;
    },

    execLogin() {
      this.executeLogin({
        username: this.login.username,
        password: this.login.password,
      });
    },
  },
};
</script>

<style lang="scss" scoped>
.opacity {
  opacity: 0.33;
  z-index: 1;
  background-color: #000000;
  width: 100%;
  height: 100%;
  position: fixed;
  left: 0;
  top: 0;
}

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

.terms {
  width: 730px;
  height: 680px;
  border-radius: 15px;
  background-color: #ffffff;
  border: solid 1px #979797;

  z-index: 10;
  position: relative;
  margin: auto;
  text-align: center;

  .logo {
    margin-top: 30px;
  }

  h1 {
    font-size: 20px;
    font-weight: 500;
    letter-spacing: -0.5px;
    text-align: center;
    color: #000000;
  }

  .terms-text {
    text-align: left;
    margin: 25px;
    font-size: 14px;
    letter-spacing: -0.3px;
    text-align: left;
    color: #000000;
    height: 390px;
    overflow-x: hidden;
    overflow-y: auto;
  }

  .l-refuse {
    border: solid 2px #9b9fa3;
  }

  .l-accept {
    border: solid 2px #00cbff;
  }
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

  small {
    font-size: 14px;
    font-weight: 500;
    letter-spacing: -0.3px;
    text-align: center;
    color: #9b9fa3;
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

  .forgot {
    font-size: 16px;
    letter-spacing: -0.4px;
    text-align: center;
    color: #00cbff;
    text-decoration: none;
  }

  .l-submit {
    border: solid 2px #7ed321;
  }

  .l-register {
    border: solid 2px #00cbff;
  }
}
</style>
