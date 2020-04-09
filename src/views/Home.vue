<template>
  <div class="home">
    <div class="columns">
      <div class="column is-narrow selection-pane">
        <drukte-tabel
          title="Top 10 drukke plekken ⚠️"
          :data="filteredData.slice(0, 10)"
        />
        <drukte-tabel
          title="Top 5 drukke parken 🌳"
          :data="
            filteredData.filter((el) => el.types.includes('park')).slice(0, 5)
          "
        />
        <drukte-tabel
          title="Top 5 drukke winkels 🛒"
          :data="
            filteredData.filter((el) => el.types.includes('store')).slice(0, 5)
          "
        />
        <div class="field">
          <h2>Categorieën ({{ filteredData.length }} items)</h2>
          <p class="selectors">
            <a @click="selectedTypes = typeUniques">Selecteer alles</a> |
            <a @click="selectedTypes = []">Deselecteer alles</a>
          </p>
          <div v-for="type in typeUniques" v-bind:key="type.id">
            <b-checkbox v-model="selectedTypes" :native-value="type"
              >{{ type }} ({{
                filteredData.filter((el) => el.types.includes(type)).length
              }})
            </b-checkbox>
            <!-- <li
              v-for="item in filteredData.filter((el) =>
                el.types.includes(type)
              )"
              v-bind:key="type.id"
            >
              {{ item.address }}
            </li> -->
          </div>
        </div>
      </div>
      <div class="column ">
        <l-map class="map" :zoom="map.zoom" :center="map.center">
          <l-control position="topright">
            <button class="button" @click="scrollToTop">^</button>
          </l-control>

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
          >
            <l-tooltip>{{ point.name }}</l-tooltip></l-circle
          >
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
  LTooltip,
  LControl,
} from "vue2-leaflet";
import "leaflet/dist/leaflet.css";
import data from "../assets/data/example.json";
import drukteTabel from "@/components/drukteTabel.vue";
import * as d3 from "d3";

export default {
  name: "home",
  data() {
    return {
      data: data
        .filter((el) => el.current_popularity > 50)
        .sort((a, b) => b.current_popularity - a.current_popularity),
      selectedTypes: [],
      typesOfInterest: ["park", "store", "hardware_store", "supermarket"],
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
    drukteTabel,
    LMap,
    LTileLayer,
    LMarker,
    LCircleMarker,
    LCircle,
    LPopup,
    LControlZoom,
    LTooltip,
    LControl,
  },
  watch: {},
  methods: {
    scrollToTop() {
      window.scrollTo(0, 0);
    },
  },
  created: function() {
    this.selectedTypes = this.typeUniques;
    // this.selectedTypes = ["supermarket"];
  },
  computed: {
    typeUniques() {
      const unwantedTypes = ["point_of_interest", "establishment"];
      const filterUnwantedTypes = (el) => !unwantedTypes.includes(el);
      const getUniques = (arr) => [...new Set(arr)];
      const types = (arr) => arr.flatMap((el) => el.types);
      return getUniques(types(this.data)).filter(filterUnwantedTypes);
    },
    filteredData() {
      return this.data.filter((el) =>
        this.selectedTypes.some((selectedCat) => el.types.includes(selectedCat))
      );
    },
    popularity2radius() {
      return d3
        .scaleSqrt()
        .domain(d3.extent(this.filteredData, (d) => d.current_popularity))
        .range([0, 400]);
    },
  },
};
</script>
<style>
.selection-pane {
  background-color: whitesmoke;
  padding: 1rem;
}
.selectors {
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

.map {
  height: 600px !important;
}
@media (min-width: 768px) {
  .map {
    height: 995px !important;
  }
}
</style>
