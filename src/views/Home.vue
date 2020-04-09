<template>
  <div class="home">
    <div class="columns">
      <div class="column is-narrow selection-pane">
        <div class="field">
          <h2>Categorieën ({{ filteredData.length }} totaal)</h2>
          <ul>
            <li v-for="type in typeUniques" v-bind:key="type.id">
              <b-checkbox v-model="selectedCategories" :native-value="type"
                >{{ type }} ({{
                  filteredData.filter((el) => el.types.includes(type)).length
                }})
              </b-checkbox>
            </li>
          </ul>
        </div>
      </div>
      <div class="column ">
        <l-map style="height: 644px" :zoom="map.zoom" :center="map.center">
          <l-tile-layer
            :url="map.url"
            :attribution="map.attribution"
          ></l-tile-layer>
          <l-circle
            v-for="point in filteredData"
            v-bind:key="point.id"
            :lat-lng="[point.coordinates.lat, point.coordinates.lng]"
            :radius="popularity2radius(point.current_popularity)"
            color="#f03"
            :opacity="0.5"
          />
        </l-map>
      </div>
    </div>
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
} from "vue2-leaflet";
import "leaflet/dist/leaflet.css";
import data from "../assets/data/example.json";
import * as d3 from "d3";

export default {
  name: "home",
  data() {
    return {
      data: data,
      selectedCategories: [],
      map: {
        refillData: [],
        zoom: 11,
        center: L.latLng(52.3702, 4.8952),
        url:
          "https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png",
        attribution: "CC-BY-4.0 Gemeente Amsterdam",
      },
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
  },
  watch: {},
  methods: {},
  created: function() {
    // this.selectedCategories = this.typeUniques;
    this.selectedCategories = ["point_of_interest"];
  },
  computed: {
    typeUniques() {
      const getUniques = (arr) => [...new Set(arr)];
      const types = (arr) => arr.flatMap((el) => el.types);
      return getUniques(types(this.data));
    },
    filteredData() {
      return (
        this.data
          // .filter((el) => el.current_popularity > 50)
          .filter((el) =>
            this.selectedCategories.some((selectedCat) =>
              el.types.includes(selectedCat)
            )
          )
      );
    },
    popularity2radius() {
      return d3
        .scaleSqrt()
        .domain(d3.extent(this.filteredData, (d) => d.current_popularity))
        .range([50, 400]);
    },
  },
};
</script>
<style>
.selection-pane {
  background-color: whitesmoke;
  padding: 1rem;
}
h2 {
  font-size: 1.3em !important;
  margin-top: 1em !important;
  margin-bottom: 0.3em !important;
  margin-left: 0.6em !important ;
  font-family: Avenir LT W01\ 85 Heavy, arial, sans-serif;
}
ul,
.block {
  margin-left: 0.8em !important ;
}
</style>
