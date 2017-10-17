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
                  <h1>Hello, Alex</h1>
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-center">
                  <input type="text" class="input" name="name" value="" placeholder="Alex Ross"/>
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-center">
                  <input type="email" class="input" name="name" value="" placeholder="ross@gmail.com"/>
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-center">
                  <h2>Change password</h2>
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-center">
                  <input type="password" class="input" name="password" placeholder="Current password"/>
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-center">
                  <input type="password" class="input" name="password" placeholder="New password"/>
                </div>
              </div>

              <div class="columns">
                <div class="column has-text-right-desktop">
                  <button type="submit" class="btn button l-submit">Save</button>
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
import HeaderIndex from '../header/Index';

export default {
  name: 'Login',

  components: { HeaderIndex },
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
