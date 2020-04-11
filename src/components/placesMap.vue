<template>
  <div>
    <l-map class="map" :zoom="map.zoom" :center="map.center">
      <l-control position="bottomright">
        <button class="button" @click="scrollToTop">^</button>
      </l-control>

      <l-tile-layer
        :url="map.url"
        :attribution="map.attribution"
      ></l-tile-layer>
      <l-circle
        v-for="point in data"
        v-bind:key="point.id"
        :lat-lng="[point.coordinates.lat, point.coordinates.lng]"
        :radius="popularity2radius(point.current_popularity)"
        :color="point.id === selectedLocation.id ? '#f03' : 'blue'"
        :opacity="0.5"
      >
        <l-tooltip
          >{{ point.name }} <br />
          Adres: {{ point.address }} <br />

          Huidige pop. score: {{ point.current_popularity }}
        </l-tooltip></l-circle
      >
    </l-map>
    <p>
      <em
        >Hoe groter de cirkel, hoe drukker de plek is dan gebruikelijk op dit
        tijdstip.</em
      >
    </p>
  </div>
</template>

<script>
import L from "leaflet";
import {
  LMap,
  LTileLayer,
  LMarker,
  LCircleMarker,
  LCircle,
  LPopup,
  LControlZoom,
  LTooltip,
  LControl
} from "vue2-leaflet";
import "leaflet/dist/leaflet.css";
import * as d3 from "d3";

export default {
  name: "kaart",
  props: ["data", "selectedLocation"],
  data() {
    return {
      map: {
        refillData: [],
        zoom: 12,
        center: L.latLng(52.3702, 4.8952),
        url:
          "https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png",
        attribution: "CC-BY-4.0 Gemeente Amsterdam"
      },
      localData: this.data
    };
  },
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LCircleMarker,
    LCircle,
    LPopup,
    LControlZoom,
    LTooltip,
    LControl
  },
  watch: {},
  methods: {
    scrollToTop() {
      window.scrollTo(0, 0);
    }
  },
  computed: {
    popularity2radius: function() {
      return d3
        .scaleSqrt()
        .domain(d3.extent(this.localData, d => d.current_popularity))
        .range([0, 400]);
    }
  }
};
</script>
<style>
.map {
  height: 600px !important;
}
@media (min-width: 768px) {
  .map {
    height: 995px !important;
  }
  .button {
    display: none !important;
  }
}
</style>
