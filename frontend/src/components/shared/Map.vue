<template>
  <v-map :zoom="zoom" :center="center" ref="map" class="map">
    <v-tilelayer :url="url" :attribution="attribution"></v-tilelayer>
    <v-marker-cluster :options="clusterOptions">
      <v-marker :key="l.text" v-for="l in locations" :lat-lng="l.latlng" :icon="icon">
        <v-popup :content="l.text"></v-popup>
      </v-marker>
    </v-marker-cluster>
  </v-map>
</template>

<script>
import L from 'leaflet';
import Vue2Leaflet from 'vue2-leaflet';
import Vue2LeafletMarkerCluster from 'vue2-leaflet-markercluster';
import markerPixel from '../../assets/img/pixel.png';

function rand(n) {
  const max = n + 0.1;
  const min = n - 0.1;
  return (Math.random() * (max - min)) + min;
}

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
    const locations = [];

    for (let i = 0; i < 100; i += 1) {
      locations.push({
        latlng: L.latLng(rand(-34.9205), rand(-57.953646)),
        text: `Hola ${i}`,
      });
    }

    const icon = L.icon({
      iconUrl: markerPixel,
      shadowUrl: 'aaa',
      iconSize: [30, 30],
      iconAnchor: [22, 94],
      popupAnchor: [-8, -90],
      shadowSize: [0, 0],
      shadowAnchor: [22, 94],
      className: 'icon-pin pin',
    });

    return {
      zoom: 11,
      url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      locations,
      icon,
      clusterOptions: {},
      center: L.latLng(-34.9205, -57.953646),
    };
  },

  mounted() {
    this.$refs.map.mapObject.zoomControl.remove();
    L.control.zoom({ minZoom: 3, position: 'topright' }).addTo(this.$refs.map.mapObject);

    setTimeout(() => {
      this.$nextTick(() => {
        // this.clusterOptions = { disableClusteringAtZoom: 11 };
      });
    }, 5000);
  },
};
</script>

<style lang="scss">
@import "~leaflet/dist/leaflet.css";
@import "~leaflet.markercluster/dist/MarkerCluster.css";
@import "~leaflet.markercluster/dist/MarkerCluster.Default.css";

.pin {
  font-size: 38px;
  color: #9013fe;
}

.map {
  z-index: 0;
  width: 100%;
  position: fixed;
  top: 78px;
  left: 0;
  bottom: 0;
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

.leaflet-touch .leaflet-bar a {
  width: 41px;
  height: 45px;
  line-height: 45px;
  color: #9b9fa3;
  font-size: 26px;
  font-weight: bolder;
}

.leaflet-bar a, .leaflet-bar a:hover {
  border-bottom: 1px solid #e4e4e4;
}
</style>
