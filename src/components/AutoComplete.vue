<template>
  <b-field label="">
    <b-autocomplete
      v-model="autocompleteInput"
      :data="data"
      ref="autocomplete"
      placeholder="bijvoorbeeld 'Eerste Ringdijkstraat 5'"
      field="_display"
      :loading="isFetching"
      :keepFirst=true
      :clearOnSelect=false
      :openOnFocus=false
      @input="getAsyncData"
      spellcheck="false"
      @select="option => selected = option"
    >
      <template slot-scope="props">
        <div class="media">
          <div class="media-content">
            {{ props.option._display }}
          </div>
        </div>
      </template>
      <template slot="empty">Nog geen resultaten gevonden</template>
    </b-autocomplete>
  </b-field>
</template>

<script>
import debounce from "lodash/debounce";
import rd2Wgs from "../assets/js/rd_to_wsg84_coordinate_conversion.js";
import polylabel from "polylabel";

export default {
  data() {
    return {
      data: [],
      bagURL: "",
      autocompleteInput: "",
      bagResult: {},
      bagResultPand: {},
      selected: null,
      coords: null,
      isFetching: false
    };
  },
  methods: {
    // Debounce to go easy on the API a bit
    flatten: function(arr) {
      while (arr.find(el => Array.isArray(el)))
        arr = Array.prototype.concat(...arr);
      return arr;
    },
    getPolyCoords: function(arr) {
      // We use polylabel to find the best place for a label inside a polygon
      // see https://github.com/mapbox/polylabel
      // A centroid isn't good for curved roads like the Herengracht
      const polyRd = polylabel(arr);
      // We use a function to convert the Dutch Rijkscoordinaten system to 'normal' wsg84 lat/longs
      const coordsSwitched = rd2Wgs(polyRd[0], polyRd[1]);
      return [coordsSwitched[1], coordsSwitched[0]];
    },
    getNormalCoords: function(arr) {
      const coordsSwitched = rd2Wgs(arr[0], arr[1]);
      return [coordsSwitched[1], coordsSwitched[0]];
    },
    getAsyncData: debounce(function() {
      if (!this.autocompleteInput.length) {
        this.data = [];
        return;
      }
      this.isFetching = true;
      this.axios
        .get(
          `https://api.data.amsterdam.nl/atlas/typeahead/bag/?format=json&q=${
            this.autocompleteInput
          }`
        )
        .then(({ data }) => {
          this.data = [];
          if (data[0]) {
            // The API contains some results we don't want, like 'bouwblok'.
            if (
              data[0]["label"] == "Straatnamen" ||
              data[0]["label"] == "Adressen"
            ) {
              data[0].content.forEach(item => this.data.push(item));
            }
          }
          this.isFetching = false;
        })
        .catch(error => {
          this.data = [];
          this.isFetching = false;
          throw error;
        });
    }, 300)
  },
  watch: {
    // We watch for changes to a selection in the autocomplete, so we can look up
    // its coordinates in the BAG API.
    selected: function() {
      if (this.selected) {
        this.bagURL = this.selected["uri"];
        this.isFetching = true;
        this.axios
          .get(`https://api.data.amsterdam.nl/${this.bagURL}?format=json`)
          .then(({ data }) => {
            this.bagResult = data;
            if (this.bagResult.geometrie.type === "MultiPolygon") {
              // Use the polylabel library to get a good place for a label inside multipolygon
              // only use the first polygon in the array (could be improved by taking
              // all polygons into account and by using the best distance)
              this.coords = this.getPolyCoords(
                this.bagResult.geometrie.coordinates[0]
              );
              this.data = [];
            } else if (
              // We can use the whole array for a polygon
              this.bagResult.geometrie.type === "Polygon"
            ) {
              this.coords = this.getPolyCoords(
                this.bagResult.geometrie.coordinates
              );
              this.data = [];
            } else if (this.bagResult.geometrie.type === "Point") {
              this.coords = this.getNormalCoords(
                this.bagResult.geometrie.coordinates
              );
              this.data = [];
            } else {
              console.error("Coordinate type not found");
            }
            this.isFetching = false;
          })
          .catch(error => {
            this.isFetching = false;
            this.data = [];
            throw error;
          });
      }
    },
    bagResult: function() {
      if (this.bagURL.includes("verblijfsobject")) {
        this.isFetching = true;
        this.axios
          .get(
            `https://api.data.amsterdam.nl/bag/pand/?verblijfsobjecten__id=${
              this.bagResult.verblijfsobjectidentificatie
            }&detailed=1&format=json`
          )
          .then(({ data }) => {
            this.data = [];
            this.bagResultPand = data;
            this.isFetching = false;
            this.$emit("selectedBAGResultPand", this.bagResultPand);
          })
          .catch(error => {
            this.isFetching = false;
            this.data = [];
            throw error;
          });
      }
    },
    coords: function() {
      this.$emit("selectedAddressCoordinates", this.coords);
      this.$emit("selectedAddress", this.selected._display);
      this.$emit("selectedBAGResult", this.bagResult);
      this.$emit("selectedBAGID", this.bagResult.verblijfsobjectidentificatie);
    }
  }
};
</script>
<style scoped>
.dropdown-menu {
  /* I need to find a better way than this :) */
  z-index: 1001 !important;
}
</style>
