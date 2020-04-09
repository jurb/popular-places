<template>
  <div>
    <l-map style="height: 644px" :zoom="map.zoom" :center="map.center">
      <l-tile-layer
        :url="map.url"
        :attribution="map.attribution"
      ></l-tile-layer>
      <l-marker
        v-for="data in filteredData"
        :key="data.id"
        :lat-lng="getL(data.lat, data.lon)"
        :icon="getIcon(data)"
        :title="data.name"
      >
        <l-popup v-if="data.name" :content="`${data.name}`"></l-popup>
        <l-popup v-else :content="'Geen naam bekend'"></l-popup>
      </l-marker>
      <l-marker
        :zIndexOffset="1000000000"
        :lat-lng="map.marker"
        :icon="map.icons.selectedAddressIcon"
      >
        <l-popup :content="selectedAddress"></l-popup>
      </l-marker>
    </l-map>
  </div>
</template>
<script>
import { LMap, LTileLayer, LMarker, LPopup, LControlZoom } from "vue2-leaflet";
import "leaflet/dist/leaflet.css";
// import LeafletHeatmap from "vue2-leaflet-heatmap";
import L from "leaflet";

export default {
  name: "LeafletMap",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
    LControlZoom,
  },
  props: {
    filteredData: Array,
    selectedAddressCoordinates: Array,
    radius: Number,
    selectedAddress: String,
  },
  data() {
    return {
      map: {
        refillData: [],
        zoom: 15,
        center: L.latLng(52.3702, 4.8952),
        url:
          "https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png",
        attribution: "CC-BY-4.0 Gemeente Amsterdam",
        marker: L.latLng(
          this.selectedAddressCoordinates[1],
          this.selectedAddressCoordinates[0]
        ),
        icons: {
          selectedAddressIcon: L.icon({
            iconUrl: require("../assets/images/markers/selectedAddress.svg"),
            iconSize: [40, 40],
            iconAnchor: [20, 39],
            popupAnchor: [0, -35],
          }),
        },
      },
    };
  },
  methods: {
    getL: function(lat, lon) {
      return L.latLng(lat, lon);
    },
    getIcon: function(data) {
      return L.icon({
        iconUrl: require(`../assets/images/markers/winkels.svg`),
        iconSize: [40, 40],
        iconAnchor: [20, 39],
        popupAnchor: [0, -35],
      });
    },
  },
  computed: {},
  watch: {
    selectedAddressCoordinates: function(data) {
      this.map.zoom = 15;
      this.map.marker = L.latLng(data[1], data[0]);
      this.map.center = L.latLng(data[1], data[0]);
    },
  },
};
</script>
<style>
.leaflet-popup-content-wrapper {
  padding: 1px;
  text-align: left;
  border-radius: 0px;
}
</style>
