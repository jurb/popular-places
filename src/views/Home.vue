<template>
  <div class="home">
    <div class="columns">
      <div class="column is-narrow selection-pane">
        <drukte-tabel
          v-on:selected="setSelectedLocation"
          :selected-location="selectedLocation"
          title="Top 10 drukke plekken ⚠️"
          :data="
            getTableData({
              data: filteredData,
              filterProperty: 'types',
              filterValue: 'point_of_interest',
              sortBy: 'current_popularity',
              numberOfRows: 10,
            })
          "
        />
        <drukte-tabel
          v-on:selected="setSelectedLocation"
          :selected-location="selectedLocation"
          title="Top 5 drukke parken 🌳"
          :data="
            getTableData({
              data: filteredData,
              filterProperty: 'types',
              filterValue: 'park',
              sortBy: 'current_popularity',
              numberOfRows: 5,
            })
          "
        />
        <drukte-tabel
          v-on:selected="setSelectedLocation"
          :selected-location="selectedLocation"
          title="Top 5 drukke winkels 🛒"
          :data="
            getTableData({
              data: filteredData,
              filterProperty: 'types',
              filterValue: 'store',
              sortBy: 'current_popularity',
              numberOfRows: 5,
            })
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
          <l-control position="bottomright">
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
            :color="point.id === selectedLocation.id ? '#f03' : 'blue'"
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
      data: data.filter((el) => el.current_popularity > 50),
      selectedTypes: [],
      selectedLocation: {},
      typesOfInterest: ["park", "store", "hardware_store", "supermarket"],
      map: {
        refillData: [],
        zoom: 12,
        center: L.latLng(52.3702, 4.8952),
        url:
          "https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png",
        attribution: "CC-BY-4.0 Gemeente Amsterdam",
      },
      hotspots: [
        "ChIJ3-yu-E3ixUcR-obflfQkYiA",
        "Ei5SZW1icmFuZHRwbGVpbiwgMTAxNyBDViBBbXN0ZXJkYW0sIE5ldGhlcmxhbmRzIi4qLAoUChIJa0KdZZUJxkcRgwm6RHoRfjkSFAoSCVV3mpS1P8ZHEY2vwLdM_QBm",
        "EjBCdWlrc2xvdGVybWVlcnBsZWluLCAxMDI1IEFtc3RlcmRhbSwgTmV0aGVybGFuZHMiLiosChQKEglrIQZE8AjGRxHjrXuALvUDYRIUChIJVXealLU_xkcRja_At0z9AGY",
        "ChIJy3MKglYIxkcRb-OM2GyApmo",
        "ChIJV7MaFnYJxkcRRsotO9L0WOI",
        "ChIJWZty4NQLxkcRNmSIszATuOA",
        "ChIJKZeiT14JxkcR0tUJvUKNBAY",
        "ChIJgTYLOoUJxkcR735HWTtRTlI",
        "ChIJfUgDKG_ixUcR_MEY4khE4Xs",
        "ChIJgVQWenbixUcRBZiubJ1c4AM",
        "Ei9aYWFuZGFtbWVycGxlaW4sIDEwMTMgWkUgQW1zdGVyZGFtLCBOZXRoZXJsYW5kcyIuKiwKFAoSCf9YDVwqCMZHEY16GSj6-fOMEhQKEglVd5qUtT_GRxGNr8C3TP0AZg",
        "ChIJy_w8o40JxkcRUCcFTTKggzU",
        "ChIJz3y0xeIJxkcRNcogBVV41Gw",
        "ChIJGVr5mwrixUcR0wyF4_ZhsjQ",
        "ChIJPx19owvixUcRG-3BcoJQN2w",
        "ChIJy_w8o40JxkcRUCcFTTKggzU",
        "ChIJz3y0xeIJxkcRNcogBVV41Gw",
        "ChIJ31vOlnIJxkcR_MEh-3Vit7Y",
        "ChIJJT7UXG0JxkcRojS17gAbszo",
        "EiJKYXZhc3RyYWF0LCBBbXN0ZXJkYW0sIE5ldGhlcmxhbmRzIi4qLAoUChIJt8HB4GwJxkcRC6OBNBKjg2kSFAoSCVV3mpS1P8ZHEY2vwLdM_QBm",
        "ChIJ3yDhlXMJxkcRXFBf6b2GjQU",
      ],
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
    setSelectedLocation: function(value) {
      this.selectedLocation = value;
    },
    getTableData: function(obj) {
      return obj.data
        .filter((el) => el[obj.filterProperty].includes(obj.filterValue))
        .slice()
        .sort((a, b) => b[obj.sortBy] - a[obj.sortBy])
        .slice(0, obj.numberOfRows);
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
