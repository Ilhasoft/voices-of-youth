<template>
  <div>
    <header-index />

    <div class="columns is-marginless">
      <div class="column is-5 sidebar is-paddingless">
        <div class="header">
          <h1>Add new report</h1>
          <small>Drag the pin to mark your report</small>
        </div>

        <div class="box-form">
          <div class="form">
            <div class="columns">
              <div class="column">
                <label for="select-theme">Select theme</label>
                <v-select v-model="themeSelected" @input="loadTagsAndUsers" :options="themeOptions"></v-select>
              </div>
            </div>

            <div class="columns" v-if="showMappers">
              <div class="column">
                <label for="select-mapper">Mapper</label>
                <v-select v-model="mapperSelected" :options="mappersOptions"></v-select>
              </div>
            </div>

            <div class="columns">
              <div class="column">
                <label for="title">Title</label>
                <input class="input" type="text" placeholder="" v-model="name">
              </div>
            </div>

            <div class="columns">
              <div class="column">
                <label for="description">Description</label>
                <textarea name="" id="" cols="30" rows="10" v-model="description"></textarea>
              </div>
            </div>

            <div class="columns">
              <div class="column">
                <label for="select-theme">Tags</label>
                <v-select v-model="tagsSelected" multiple :value.sync="selected" :options="tagsOptions"></v-select>
              </div>
            </div>

            <div class="columns">
              <div class="column size">
                <label for="select-theme">Add photos and videos</label>
                <ul class="images">
                  <li>
                    <button class="new-file" @click.prevent="openFile" @mouseover="isWarningVisible = true" @mouseout="isWarningVisible = false">
                      <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 28 28">
                        <path fill="#C7C7C7" fill-rule="evenodd" d="M17.126 10.8V4.493a3.602 3.602 0 0 0-7.204 0V10.8h-6.31a3.602 3.602 0 1 0 0 7.205h6.31v6.309a3.602 3.602 0 0 0 7.205 0v-6.31h6.309a3.602 3.602 0 0 0 0-7.204h-6.31z"/>
                      </svg>
                    </button>
                    <input type="file" name="file" @change="addFileToUpload" id="file" ref="fileInput" style="display: none;" />
                  </li>

                  <file-item
                    :file="item"
                    :index="key"
                    :key="key"
                    v-for="(item, key) in files"
                    @remove-file="removeFile(item)"/>
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

                <div class="columns">
                  <div class="column is-10"><input class="input" value="link" type="text" v-model="link"></div>
                  <div class="column t-center">
                    <button class="btn-link" @click.prevent="addLink">
                      <svg xmlns="http://www.w3.org/2000/svg" width="21" height="17" viewBox="0 0 21 17">
                        <path fill="none" fill-rule="evenodd" stroke="#FFF" stroke-linecap="round" stroke-linejoin="round" stroke-width="5" d="M18.116 2.74l-10.117 11-4.599-5"/>
                      </svg>
                    </button>
                  </div>
                </div>

                <link-item
                  :url="item"
                  :index="key"
                  :key="key"
                  v-for="(item, key) in urls"
                  @remove-url="removeUrl(item)"/>
              </div>
            </div>
          </div>

          <div class="buttons">
            <div class="columns is-mobile">
              <div class="column">
                <button class="cancel" @click.prevent="closeForm">Cancel</button>
              </div>

              <div class="column">
                <button class="send" @click.prevent="saveReport()">{{ btnSendName }}</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="column is-paddingless map-report">
        <v-map :zoom="3" :minZoom="3" :maxZoom="18" :options="optionsMap" :center="center" ref="map">
          <v-tilelayer :url="url" :attribution="attribution" :options="options"></v-tilelayer>
        </v-map>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import vSelect from 'vue-select';

import L from 'leaflet';
import Vue2Leaflet from 'vue2-leaflet';
import Vue2LeafletMarkerCluster from 'vue2-leaflet-markercluster';

import router from '@/router/';
import markerPixel from '@/assets/img/map-pin.png';
import HeaderIndex from '@/components/header/Index';
import LinkItem from '@/components/new-report/Link';
import FileItem from '@/components/new-report/File';

export default {
  name: 'NewReport',

  components: {
    HeaderIndex,
    LinkItem,
    FileItem,
    vSelect,
    'v-map': Vue2Leaflet.Map,
    'v-tilelayer': Vue2Leaflet.TileLayer,
    'v-marker': Vue2Leaflet.Marker,
    'v-popup': Vue2Leaflet.Popup,
    'v-marker-cluster': Vue2LeafletMarkerCluster,
  },

  data() {
    return {
      selected: null,

      isWarningVisible: false,
      name: '',
      description: '',
      link: '',
      location: {},
      themeSelected: 0,
      mapperSelected: 0,
      mappersOptions: [],
      tagsSelected: [],
      tagsOptions: [],
      files: [],
      urls: [],
      showMappers: false,

      marker: null,
      options: { noWrap: true },
      optionsMap: { maxBounds: [[-90, -160], [90, 160]] },
      url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      center: [0, 0],

      icon: L.icon({
        iconUrl: markerPixel,
        shadowUrl: '',
        iconSize: [36, 54],
        iconAnchor: [16, 54],
        popupAnchor: [-0, -90],
        shadowSize: [0, 0],
        shadowAnchor: [22, 94],
      }),

      btnSendName: 'Send report',
      btnSendDisabled: '',
      polygonMap: null,
    };
  },

  mounted() {
    if (!this.userIsLogged) {
      router.push({ name: 'login' });
    } else if (this.userIsMapper === false) {
      router.push({ name: 'project', params: { path: this.currentProject.path } });
    } else {
      if (this.currentUser.is_admin) {
        this.showMappers = true;
        this.getProjectThemes();
      } else if (this.currentUser.is_mapper) {
        this.getUserThemes(this.currentUser.id);
      }

      this.$refs.map.mapObject.zoomControl.remove();
      L.control.zoom({ minZoom: 3, position: 'topright' }).addTo(this.$refs.map.mapObject);

      this.marker = L.marker(this.center, { icon: this.icon, draggable: true })
        .addTo(this.$refs.map.mapObject);

      this.marker.on('move', (event) => {
        this.location = {
          type: 'Point',
          coordinates: [event.latlng.lng, event.latlng.lat],
        };
      });

      this.$refs.map.mapObject.on('click', (event) => {
        this.marker.setLatLng(event.latlng).update();
      });
    }
  },

  computed: {
    ...mapGetters({
      currentUser: 'getUserData',
      userIsLogged: 'userIsLogged',
      userIsMapper: 'userIsMapper',
      themes: 'getUserThemes',
      currentProject: 'getCurrentProject',
    }),

    themeOptions() {
      return this.themes.map((theme) => {
        const option = {
          label: theme.name,
          value: theme.id,
        };
        return option;
      });
    },
  },

  methods: {
    ...mapActions([
      'getUserThemes',
      'getProjectThemes',
      'getUsersByTheme',
      'saveNewReport',
      'saveFiles',
      'notifyOpen',
    ]),

    openFile() {
      this.$refs.fileInput.click();
    },

    lockButtonSend() {
      this.btnSendName = 'Wait please';
      this.btnSendDisabled = true;
    },

    unlockButtonSend() {
      this.btnSendName = 'Send report';
      this.btnSendDisabled = false;
    },

    cleanForm() {
      this.name = '';
      this.description = '';
      this.themeSelected = '';
      this.mapperSelected = '';
      this.tagsSelected = [];
      this.tagsOptions = [];
      this.files = [];
      this.urls = [];
      this.notifyOpen({ type: 1, message: 'Report Sent!' });
    },

    uploadPreventDefault(e) {
      e.stopPropagation();
      e.preventDefault();
    },

    removeFile(file) {
      this.files.splice(this.files.indexOf(file), 1);
    },

    addFileToUpload(e) {
      this.uploadPreventDefault(e);
      const file = e.target.files || e.dataTransfer.files;
      if (file[0].type === 'image/jpeg' || file[0].type === 'image/png') {
        const reader = new FileReader();
        reader.onload = (f) => {
          this.files.push({
            item: file,
            blob: f.target.result,
          });
        };
        reader.readAsDataURL(file[0]);
      }
    },

    addLink() {
      if (this.link) {
        if (!/^https?:\/\//i.test(this.link)) {
          this.link = `http://${this.link}`;
        }
        this.urls.push(this.link);
        this.link = '';
      }
    },

    removeUrl(url) {
      this.urls.splice(this.urls.indexOf(url), 1);
    },

    loadTagsAndUsers(select) {
      if (select) {
        this.tagsSelected = [];
        const data = this.themes.filter(item => item.id === select.value);

        if (data.length > 0) {
          const theme = data[0];
          this.tagsOptions = theme.tags.map(tag => tag);

          if (this.polygonMap) {
            this.$refs.map.mapObject.removeLayer(this.polygonMap);
          }

          if (theme) {
            this.polygonMap = new L.Polygon(theme.bounds);
            this.polygonMap.setStyle({ color: `#${theme.color}` });
            this.$refs.map.mapObject.addLayer(this.polygonMap);
            this.$refs.map.mapObject.fitBounds(this.polygonMap.getBounds());
            this.marker.setLatLng(this.polygonMap.getBounds().getCenter());
          }
        }

        if (this.currentUser.is_admin && this.themeSelected.value > 0) {
          this.getUsersByTheme(this.themeSelected.value).then((users) => {
            this.mappersOptions = users.map((user) => {
              const option = {
                label: user.username,
                value: user.id,
              };
              return option;
            });
          });
        }
      }
    },

    saveReport() {
      if (this.name && this.description && this.themeSelected && this.location) {
        this.lockButtonSend();

        const dataToSave = {
          name: this.name,
          description: this.description,
          theme: this.themeSelected.value,
          tags: this.tagsSelected,
          location: this.location,
          urls: this.urls,
        };

        if (this.currentUser.is_admin) {
          dataToSave.mapper_id = this.mapperSelected.value;
        }

        this.saveNewReport(dataToSave).then((data) => {
          if (this.files.length > 0) {
            const promiseAll = this.files.map((file) => {
              const promiseUpload = new Promise((resolve, reject) => {
                this.saveFiles({
                  id: data.id,
                  file: file.item[0],
                }).then(() => resolve(),
                ).catch(() => reject());
              });
              return promiseUpload;
            });

            Promise.all(promiseAll).then(() => {
              this.cleanForm();
              this.unlockButtonSend();
            });
          } else {
            this.cleanForm();
            this.unlockButtonSend();
          }
        }).catch(() => {
          this.unlockButtonSend();
        });
      }
    },

    closeForm() {
      router.push({ name: 'project', params: { path: this.currentProject.path } });
    },
  },
};
</script>

<style lang="scss" scoped>
@import "~leaflet/dist/leaflet.css";
@import "~leaflet.markercluster/dist/MarkerCluster.css";
@import "~leaflet.markercluster/dist/MarkerCluster.Default.css";

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

.map-report {
  height: 91vh;
  z-index: 0;
}

.sidebar {
  box-shadow: 0 9px 10px 0 rgba(0, 0, 0, 0.16);
  height: 91vh;

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
        outline: none;
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
