<template>
  <mapbox access-token="pk.eyJ1IjoianVyaWFuIiwiYSI6ImNqNTJlMTAzYzBmajEyd242ank0ZGppam8ifQ.JlOhR91CJQnc3U12pbMQwQ" :map-options="{
      style: 'mapbox://styles/mapbox/light-v9',
      center: [4.8952, 52.3702],
      zoom: 12
	}" :geolocate-control="{
  show: true,
  position: 'top-left'
}" :scale-control="{
  show: true,
  position: 'top-left'
}" :fullscreen-control="{
  show: true,
  position: 'top-left'
}"></mapbox>
</template>

<script>
import Mapbox from "mapbox-gl-vue";
// import p2000Data from "../assets/data/p2000.json";

export default {
  components: {
    Mapbox
  },
  data() {
    return {};
  }
};
</script>

<style>
@import url("//api.tiles.mapbox.com/mapbox-gl-js/v0.46.0/mapbox-gl.css");
#map {
  width: 100%;
  height: 500px;
}
</style>
