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
                  <img src="~@/assets/img/login-a.png" alt="">
                </div>
              </div>

              <form action="" @submit.prevent="userLogin()">
                <div class="columns">
                  <div class="column has-text-center">
                    <h1>{{ $t('message.pages.login.title') }}</h1>
                    <small>{{ $t('message.pages.login.subtitle') }}</small>
                  </div>
                </div>

                <div class="columns">
                  <div class="column has-text-center">
                    <input type="text" class="input" name="name" value="" :placeholder="$t('message.pages.login.username')" v-model="login.username"/>
                  </div>
                </div>

                <div class="columns">
                  <div class="column has-text-center">
                    <input type="password" class="input" name="password" :placeholder="$t('message.pages.login.password')" v-model="login.password"/>
                  </div>
                </div>

                <div class="columns">
                  <div class="column has-text-center">
                    {{ $t('message.pages.login.remember') }}
                  </div>
                </div>

                <div class="columns">
                  <div class="column has-text-center">
                    <button type="submit" @click.prevent="userLogin()" class="btn button l-submit">{{ $t('message.pages.login.btnLogin') }}</button>
                  </div>
                </div>
              </form>
            </div>
          </article>
        </div>

        <div class="tile is-parent">
          <article class="tile is-child">
            <div class="content">
              <div class="columns">
                <div class="column has-text-center">
                  <img src="~@/assets/img/login-b.png" alt="">
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-center">
                  <h1>{{ $t('message.pages.register.title') }}</h1>
                  <small>{{ $t('message.pages.register.subtitle') }}</small>
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-center">
                  <input type="text" class="input" v-model="register.name" :placeholder="$t('message.pages.register.name')"/>
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-center">
                  <input type="text" class="input" v-model="register.username" :placeholder="$t('message.pages.register.username')"/>
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-center">
                  <input type="email" class="input" v-model="register.email" :placeholder="$t('message.pages.register.email')"/>
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-center">
                  <input type="password" minlength="6" class="input" v-model="register.password" :placeholder="$t('message.pages.register.password')"/>
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-center">
                  <input type="password" minlength="6" class="input" v-model="register.confirmPassword" :placeholder="$t('message.pages.register.confirmPassword')"/>
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-center">
                  <label class="checkbox">
                    <input type="checkbox" v-model="isAccepted">
                    {{ $t('message.pages.register.terms') }}
                  </label>
                </div>

                <div class="column has-text-center">
                  <button
                    type="submit"
                    @click.prevent="openTerms"
                    class="btn button l-register">
                    {{ $t('message.pages.register.btnRegister') }}
                  </button>
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
            <img src="~@/assets/img/logo.png" class="logo" alt="">
          </div>
        </div>

        <div class="columns">
          <div class="column is-paddingless">
            <h1>{{ $t('message.pages.register.termsBox.title') }}</h1>
          </div>
        </div>

        <div class="columns">
          <div class="column">
            <div class="terms-text">
              <p>{{ $t('message.pages.register.termsBox.description') }}</p>
            </div>
          </div>
        </div>

        <div class="columns">
          <div class="column has-text-center">
            <button
              class="btn button l-refuse"
              @click.prevent="closeTerms(false)">
              {{ $t('message.pages.register.termsBox.refuse') }}
            </button>
          </div>

          <div class="column has-text-center">
            <button
              class="btn button l-accept"
              @click.prevent="closeTerms(true)">
              {{ $t('message.pages.register.termsBox.accept') }}
            </button>
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

export default {
  name: 'Login',

  components: { HeaderIndex },

  data() {
    return {
      isOpened: false,
      isAccepted: true,

      login: {
        username: '',
        password: '',
      },

      register: {
        name: '',
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
      },
    };
  },

  computed: {
    ...mapGetters({
      currentProject: 'getCurrentProject',
    }),
  },

  methods: {
    ...mapActions([
      'executeLogin',
      'notifyOpen',
      'executeRegisterProfile',
    ]),

    openTerms() {
      this.isOpened = !this.isOpened;
    },

    closeTerms(value) {
      this.isOpened = false;
      this.isAccepted = value;

      if (value) {
        this.userRegister();
      }
    },

    userLogin() {
      this.executeLogin({
        username: this.login.username,
        password: this.login.password,
      }).then((response) => {
        if (response) {
          router.push({ name: 'project', params: { path: this.currentProject.path } });
        }
      }).catch((error) => {
        this.notifyOpen({ type: 0, message: error.response.data.non_field_errors[0] });
      });
    },

    userRegister() {
      if (this.isAccepted) {
        this.executeRegisterProfile(this.register).then(() => {
          this.register = {
            name: '',
            username: '',
            email: '',
            password: '',
            confirmPassword: '',
          };
        }).catch(() => {});
      }
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
  text-align: center;

  position: absolute;
  margin: auto;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;

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
