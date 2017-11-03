import axios from 'axios';
// import { urlAPI } from '../helper';

export default {
  state: {
    userData: {},
    isLogged: false,
  },

  getters: {
    getUserData: state => state.userData,
    userIsLogged: state => state.isLogged,
  },

  actions: {
    executeLogin({ commit }, obj) {
      // const data = JSON.stringify({
      //   username: obj.username,
      //   password: obj.password,
      // });

      // const xhr = new XMLHttpRequest();
      // xhr.withCredentials = true;

      // xhr.addEventListener('readystatechange', () => {
      //   if (this.readyState === 4) {
      //     console.log(this.responseText);
      //   }
      // });

      // xhr.open('POST', 'http://192.168.0.155:8000/api/get_auth_token/');
      // xhr.setRequestHeader('content-type', 'application/json');
      // xhr.send(data);

      axios.post('http://192.168.0.155:8000/api/get_auth_token/', {
        username: obj.username,
        password: obj.password,
      }).then((response) => {
        console.log(response.data);
      }).catch((error) => {
        throw new Error(error);
      });

      // axios.request({
      //   url: 'http://localhost:8000/api/get_auth_token/',
      //   method: 'post',
      //   data: {
      //     username: obj.username,
      //     password: obj.password,
      //   },
      //   headers: {
      //     'content-type': 'application/json',
      //   },
      // }).then((response) => {
      //   console.log(response.data);
      //   // commit(TYPES.SET_THEMES, response.data);
      // }).catch((error) => {
      //   throw new Error(error);
      // });
    },
  },
};
