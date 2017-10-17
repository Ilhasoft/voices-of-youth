<template>
  <div>
    <header-index />

    <div class="sidebar">
      <div class="header">
        <h1>Add new report</h1>
        <small>Drag the pin to mark your report</small>
      </div>

      <div class="box-form">
        <div class="form">

          <div class="columns">
            <div class="column">
              <label for="select-theme">Select theme</label>
              <v-select :value.sync="selected" :options="options"></v-select>
            </div>
          </div>

          <div class="columns">
            <div class="column">
              <label for="title">Title</label>
              <input class="input" type="text" placeholder="Sustainable practices that help in the development of a community">
            </div>
          </div>

          <div class="columns">
            <div class="column">
              <label for="title">Description</label>
              <textarea name="" id="" cols="30" rows="10"></textarea>
            </div>
          </div>

          <div class="columns">
            <div class="column">
              <label for="select-theme">Tags</label>
              <v-select multiple :value.sync="selected" :options="options"></v-select>

            </div>
          </div>

          <div class="columns">
            <div class="column size">
              <label for="select-theme">Add photos and videos</label>
              <ul class="images">
                <li>
                  <button class="new-file" @mouseover="isWarningVisible = true" @mouseout="isWarningVisible = false">
                    <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 28 28">
                      <path fill="#C7C7C7" fill-rule="evenodd" d="M17.126 10.8V4.493a3.602 3.602 0 0 0-7.204 0V10.8h-6.31a3.602 3.602 0 1 0 0 7.205h6.31v6.309a3.602 3.602 0 0 0 7.205 0v-6.31h6.309a3.602 3.602 0 0 0 0-7.204h-6.31z"/>
                    </svg>
                  </button>
                </li>
                
                <file-item />
              </ul>
            </div>
          </div>

          <div class="warning" :class="[isWarningVisible ? 'fade-in' : 'fade-out']">
            <div class="point"></div>
            <div class="content">
              <p>
                Remember, use only your own photos or photos that you are allowed to use
              </p>
            </div>
          </div>

          <div class="columns">
            <div class="column">
              <label for="select-theme">Add link from website</label>

              <link-item />

              <div class="columns">
                <div class="column is-10"><input class="input" type="text"></div>
                <div class="column t-center">
                  <button class="btn-link">
                    <svg xmlns="http://www.w3.org/2000/svg" width="21" height="17" viewBox="0 0 21 17">
                      <path fill="none" fill-rule="evenodd" stroke="#FFF" stroke-linecap="round" stroke-linejoin="round" stroke-width="5" d="M18.116 2.74l-10.117 11-4.599-5"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="buttons">
          <div class="columns is-mobile">
            <div class="column">
              <button class="cancel">Cancel</button>
            </div>

            <div class="column">
              <button class="send">Send report</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import vSelect from 'vue-select';

import HeaderIndex from '../header/Index';
import LinkItem from '../new-report/Link';
import FileItem from '../new-report/File';

export default {
  name: 'NewReport',

  components: { HeaderIndex, LinkItem, FileItem, vSelect },

  data() {
    return {
      selected: null,
      options: ['foo', 'bar', 'baz'],
      isWarningVisible: false,
    };
  },
};
</script>

<style lang="scss" scoped>
.images li {
  display: inline-block;
  margin-right: 12px;
  margin-bottom: 12px;
  margin-top: 20px;
  outline: none;
  position: relative;
  vertical-align: top;
}

.v-select {
  width: 100%;
  background-color: #fff;
}

.sidebar {
  width: 622px;
  box-shadow: 0 9px 10px 0 rgba(0, 0, 0, 0.16);
  position: absolute;
  margin: auto;
  top: 78px;
  left: 0;
  bottom: 0;
  background-color: #fbfbfb;
  z-index: 10000;

  .box-form {
    height: 86%;
    position: relative;

    .form {
      width: 100%;
      height: 91.6%;
      background-color: #fbfbfb;
      margin: 0 auto;
      overflow: auto;
      padding: 10px 43px 43px 43px;

      .t-center {
        text-align: center;
      }

      .warning {
        height: 53px;
        width: 250px;
        position: relative;
        margin-top: -32px;

        .point {
          margin-bottom: -12px;
          margin-left: 34px;
          width: 18px;
          height: 18px;
          background-color: #de486b;
          transform: rotate(45deg);
        }

        .content {
          padding: 6px;
          background-color: #de486b;
          border-radius: 6px;
        }

        p {
          font-size: 14px;
          letter-spacing: -0.3px;
          text-align: left;
          color: #ffffff;
        }
      }

      .size {
        width: 100%;
      }

      .new-file {
        width: 86px;
        height: 86px;
        border-radius: 10px;
        background-color: #ffffff;
        border: solid 1px #d7d7d7;
        float: left;
        margin-right: 5px;
        cursor: pointer;
      }

      ul {
        margin: 0;
        padding: 0;
        white-space: nowrap;
        overflow-x: auto;
      }

      label {
        font-size: 15px;
        font-weight: 500;
        letter-spacing: -0.4px;
        color: #000000;
        display: block;
        padding-bottom: 2px;
      }

      .btn-link {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        background-color: #9b9fa3;
        border: 0;
        outline: none;
        cursor: pointer;
      }

      input {
        height: 36px;
        border-radius: 4px;
        border: 1px solid rgba(60,60,60,.26);
      }

      textarea {
        font-size: 16px;
        letter-spacing: -0.4px;
        text-align: left;
        color: #4a4a4a;
        outline: none;
        resize: none;
        width: 100%;
        height: 80px;
        border-radius: 4px;
        background-color: #fff;
        border: 1px solid rgba(60,60,60,.26);
      }
    }

    .buttons {
      width: 100%;
      height: 75px;
      background-color: #fbfbfb;
      text-align: center;
      position: relative;

      button {
        outline: none;
        cursor: pointer;
        font-size: 18px;
        font-weight: 500;
        letter-spacing: -0.4px;
        text-align: center;
        color: #4a4a4a;
        background-color: #fbfbfb;
      }

      .cancel {
        width: 208px;
        height: 51px;
        border-radius: 100px;
        border: solid 2px #00cbff;
      }

      .send {
        width: 208px;
        height: 51px;
        border-radius: 100px;
        border: solid 2px #7ed321;
      }
    }
  }

  .header {
    height: 108px;
    background-color: #00cbff;
    text-align: center;
    margin: auto;
    padding-top: 10px;

    h1 {
      font-size: 30px;
      font-weight: bold;
      letter-spacing: -0.8px;
      text-align: center;
      color: #ffffff;
    }

    small {
      font-size: 14px;
      font-weight: 500;
      letter-spacing: -0.4px;
      text-align: center;
      color: #ffffff;
    }
  }
}
</style>
