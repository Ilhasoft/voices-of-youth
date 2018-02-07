<template>
  <v-map :zoom="3" :minZoom="3" :maxZoom="18" :options="optionsMap" :center="center" ref="map">
    <v-tilelayer :url="url" :attribution="attribution" :options="options"></v-tilelayer>
    <v-marker-cluster :options="optionsCluster">
      <v-marker @l-click="openReport(item)" :key="item.text" v-for="item in reports" :lat-lng="item.latlng" :icon="item.icon" />
    </v-marker-cluster>
  </v-map>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import L from 'leaflet';
import Vue2Leaflet from 'vue2-leaflet';
import Vue2LeafletMarkerCluster from 'vue2-leaflet-markercluster';
import bus from '@/helper/bus';

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
      optionsMap: {
        maxBounds: [
          [-85.0, -180.0],
          [85.0, 180.0],
        ],
      },
      url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      center: [0, 0],
      optionsCluster: {
        disableClusteringAtZoom: 17,
        animate: false,
      },
    };
  },

  mounted() {
    this.$refs.map.mapObject.zoomControl.remove();
    L.control.zoom({ minZoom: 3, position: 'topright' }).addTo(this.$refs.map.mapObject);

    bus.$on('openReport', (item) => {
      this.$refs.map.mapObject.setView({
        lat: item.location.coordinates[1],
        lng: item.location.coordinates[0],
      });
      this.getReport(item.id);
    });
  },

  computed: mapGetters({
    reports: 'getReportsPins',
  }),

  watch: {
    reports() {
      const bounds = this.reports.map(item => [item.latlng.lat, item.latlng.lng]);
      this.$refs.map.mapObject.flyToBounds(bounds);
    },
  },

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
        if (this.$refs.map) {
          this.$refs.map.mapObject.setView(marker.latlng);
          this.getReport(item.id);
        }
      });
    },
  },
};
</script>

<style lang="scss" scoped>
@import "~leaflet/dist/leaflet.css";
@import "~leaflet.markercluster/dist/MarkerCluster.css";
@import "~leaflet.markercluster/dist/MarkerCluster.Default.css";

.pin {
  font-size: 38px;
}
</style>
