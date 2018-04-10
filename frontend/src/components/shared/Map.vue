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

    const bounds = this.reports.map(item => [item.latlng.lat, item.latlng.lng]);
    this.$refs.map.mapObject.fitBounds(bounds);
  },

  computed: {
    ...mapGetters({
      reports: 'getReportsPins',
      report: 'getReport',
      sideBarActived: 'getSideBarIsActived',
      currentProject: 'getCurrentProject',
    }),
  },

  watch: {
    report() {
      if (this.report && this.report.location) {
        const moveTo = L.latLng(
          this.report.location.coordinates[1],
          this.report.location.coordinates[0],
        );
        const zoom = this.$refs.map.mapObject.getZoom();
        this.$refs.map.mapObject.flyTo(moveTo, (zoom < 5 ? 11 : zoom));
      }
    },

    sideBarActived() {
      if (!this.sideBarActived) {
        this.$refs.map.mapObject.invalidateSize();
      }
    },
  },

  methods: {
    ...mapActions([
      'setSideBarConfigs',
      'getReport',
      'setSearchQuery',
    ]),

    openReport(item) {
      this.setSearchQuery('');
      this.setSideBarConfigs({
        tabActived: 'ReportDetail',
        isActived: true,
      }).then(() => {
        if (this.$refs.map) {
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
