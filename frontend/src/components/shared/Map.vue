<template>
  <v-map :zoom="3" :minZoom="3" :maxZoom="20" :bounds="bounds" :center="center" ref="map" class="map">
    <v-tilelayer :url="url" :attribution="attribution" :options="options"></v-tilelayer>
    <v-marker-cluster>
      <v-marker @l-click="clickMarker(item)" :key="item.text" v-for="item in getMarkers" :lat-lng="item.latlng" :icon="item.icon">
        <v-popup :content="item.text"></v-popup>
      </v-marker>
    </v-marker-cluster>
  </v-map>
</template>

<script>
import L from 'leaflet';
import Vue2Leaflet from 'vue2-leaflet';
import Vue2LeafletMarkerCluster from 'vue2-leaflet-markercluster';
import markerPixel from '../../assets/img/pixel.png';

export default {
  name: 'Map',

  components: {
    'v-map': Vue2Leaflet.Map,
    'v-tilelayer': Vue2Leaflet.TileLayer,
    'v-marker': Vue2Leaflet.Marker,
    'v-popup': Vue2Leaflet.Popup,
    'v-marker-cluster': Vue2LeafletMarkerCluster,
  },

  props: {
    markers: {
      type: Array,
      required: true,
    },
  },

  data() {
    return {
      options: { noWrap: true },
      url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      center: null,
      bounds: L.latLngBounds(),
    };
  },

  mounted() {
    this.$refs.map.mapObject.zoomControl.remove();
    L.control.zoom({ minZoom: 3, position: 'topright' }).addTo(this.$refs.map.mapObject);
  },

  computed: {
    getMarkers() {
      const locations = Object.keys(this.markers).map((key, index) => {
        const item = {
          latlng: L.latLng(this.markers[index].location[0], this.markers[index].location[1]),
          text: this.markers[index].name,
          icon: L.icon({
            iconUrl: markerPixel,
            shadowUrl: 'none',
            iconSize: [30, 30],
            iconAnchor: [22, 94],
            popupAnchor: [-8, -90],
            shadowSize: [0, 0],
            shadowAnchor: [22, 94],
            className: 'icon-pin pin',
            styleColorName: `#${this.markers[index].theme_color}`,
          }),
        };
        return item;
      });

      Promise.all(locations).then(() => {
        this.bounds = L.latLngBounds(locations.map(o => o.latlng));
      });

      return locations;
    },
  },

  methods: {
    clickMarker(item) {
      const marker = JSON.parse(JSON.stringify(item));
      this.$refs.map.mapObject.setView(marker.latlng);
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
