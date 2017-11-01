<template>
  <v-map :zoom="3" :minZoom="3" :maxZoom="20" :bounds="bounds" :options="optionsMap" :center="center" ref="map" class="map">
    <v-tilelayer :url="url" :attribution="attribution" :options="options"></v-tilelayer>
    <v-marker-cluster>
      <v-marker @l-click="openReport(item)" :key="item.text" v-for="item in getMarkers" :lat-lng="item.latlng" :icon="item.icon" />
    </v-marker-cluster>
  </v-map>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import L from 'leaflet';
import Vue2Leaflet from 'vue2-leaflet';
import Vue2LeafletMarkerCluster from 'vue2-leaflet-markercluster';
import markerPixel from '../../assets/img/pixel.png';
import bus from '../../helper/bus';

export default {
  name: 'Map',

  components: {
    'v-map': Vue2Leaflet.Map,
    'v-tilelayer': Vue2Leaflet.TileLayer,
    'v-marker': Vue2Leaflet.Marker,
    'v-popup': Vue2Leaflet.Popup,
    'v-marker-cluster': Vue2LeafletMarkerCluster,
  },

  data() {
    return {
      options: { noWrap: true },
      optionsMap: { maxBounds: [[-90, -160], [90, 160]] },
      url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      center: null,
      bounds: L.latLngBounds(),
    };
  },

  mounted() {
    this.$refs.map.mapObject.zoomControl.remove();
    L.control.zoom({ minZoom: 3, position: 'topright' }).addTo(this.$refs.map.mapObject);

    bus.$on('openReport', (item) => {
      this.$refs.map.mapObject.setView(item.location);
      this.getReport(item.id);
    });
  },

  computed: mapState({
    themesSelected: state => state.ReportStore.themes,

    getMarkers(state) {
      const reports = state.ReportStore.all;
      const locations = Object.keys(reports).map((key, index) => {
        const item = {
          id: reports[index].id,
          latlng: L.latLng(reports[index].location[0], reports[index].location[1]),
          text: reports[index].name,
          color: reports[index].theme_color,
          icon: L.icon({
            iconUrl: markerPixel,
            shadowUrl: markerPixel,
            iconSize: [30, 30],
            iconAnchor: [22, 94],
            popupAnchor: [-8, -90],
            shadowSize: [0, 0],
            shadowAnchor: [22, 94],
            className: 'icon-pin pin',
            styleColorName: `#${reports[index].theme_color}`,
          }),
        };
        return item;
      });

      Promise.all(locations).then(() => {
        this.bounds = L.latLngBounds(locations.map(o => o.latlng));
      });

      return locations;
    },
  }),

  methods: {
    ...mapActions([
      'setSideBarConfigs',
      'getReport',
    ]),

    openReport(item) {
      this.setSideBarConfigs({
        tabActived: 'ReportDetail',
        isActived: true,
      }).then(() => {
        const marker = JSON.parse(JSON.stringify(item));
        this.$refs.map.mapObject.setView(marker.latlng);
        this.getReport(item.id);
      });
    },
  },
};
</script>

<style lang="scss">
@import "~leaflet/dist/leaflet.css";
@import "~leaflet.markercluster/dist/MarkerCluster.css";
@import "~leaflet.markercluster/dist/MarkerCluster.Default.css";

.pin {
  font-size: 38px;
}

.map {
  z-index: 0;
  width: 100%;
  position: fixed;
  left: 0;
  right: 0;
}

.leaflet-touch .leaflet-control-layers, .leaflet-touch .leaflet-bar {
  border: none !important;
}

.leaflet-control-zoom-in {
  border-top-left-radius: 100px !important;
  border-top-right-radius: 100px !important;
}

.leaflet-bar a:last-child {
  border-bottom-left-radius: 100px !important;
  border-bottom-right-radius: 100px !important;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.3);
}

.leaflet-bar a {
  width: 45px !important;
  height: 45px !important;
  line-height: 45px;
  color: #9b9fa3;
  font-size: 26px;
  font-weight: bolder;
}

.leaflet-touch .leaflet-bar a {
  width: 45px !important;
  height: 45px !important;
  line-height: 45px;
  color: #9b9fa3;
  font-size: 26px;
  font-weight: bolder;
}

.leaflet-bar a, .leaflet-bar a:hover {
  border-bottom: 1px solid #e4e4e4;
  color: #9b9fa3;
  font-size: 26px;
  font-weight: bolder;
  line-height: 45px;
}

.leaflet-bar {
  box-shadow: none;
  border-radius: 4px;
}
</style>
