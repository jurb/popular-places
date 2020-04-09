<template>
  <div class="home">
    <div class="columns is-gapless">
      <div class="column is-narrow selection-pane">
        <AutoComplete
          @selectedAddressCoordinates="updateSelectedAddressCoordinates"
          @selectedAddress="updateSelectedAddress"
          @selectedBAGResult="updateSelectedBAGResult"
          @selectedBAGResultPand="updateSelectedBAGResultPand"
          @selectedBAGID="updateSelectedBAGID"
        />
        <BagEigenschappen
          v-if="bagIsWoning"
          :title=" 'Eigenschappen woning' "
          :selectedBAGResult="selectedBAGResult"
          :selectedBAGResultPand="selectedBAGResultPand"
        />
        <RadioPane
          @selected="updateSelectedRadio"
          :categories="sortedCats"
          :title=" 'Meldingen' "
        />
        <FilterPane
          @selected="updateSelectedFilters"
          :categories="sortedCats"
          :title=" 'Voorzieningen' "
        />
      </div>
      <div class="column ">
        <LeafletMap
          :draw-heatmap="drawHeatmap"
          :filtered-data="filteredData"
          :selected-address-coordinates="selectedAddressCoordinates"
          :selected-address="selectedAddress"
          :radius="radius"
          :heatmap-data="filteredHeatmapData"
        />
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import AutoComplete from "@/components/AutoComplete.vue";
import FilterPane from "@/components/FilterPane.vue";
import RadioPane from "@/components/RadioPane.vue";
import BagEigenschappen from "@/components/BagEigenschappen.vue";
import LeafletMap from "@/components/LeafletMap.vue";
// import MapboxMap from "@/components/MapboxMap.vue";
import functionData from "../assets/data/functies.json";
import functionCategories from "../assets/data/functies-categories.json";
// prepare a singular locationData object in case we want to merge more sources later
const locationData = functionData;
const locationCategories = functionCategories;
const haversine = require("haversine");
import p2000Amsterdam from "../assets/data/p2000Amsterdam.json";

export default {
  name: "home",
  data() {
    return {
      heatmapData: p2000Amsterdam,
      locationCategories: locationCategories,
      functionData: locationData,
      selectedCategories: [],
      selectedRadio: "Uit",
      selectedAddressCoordinates: [4.8952, 52.3702],
      selectedAddress: "Oudezijds Achterburgwal 194-1",
      selectedBAGID: "03630000759242",
      radius: 0.5,
      drawHeatmap: false,
      selectedBAGResult: {},
      selectedBAGResultPand: {},
      bagIsWoning: false
    };
  },
  components: {
    AutoComplete,
    LeafletMap,
    FilterPane,
    RadioPane,
    BagEigenschappen
  },
  watch: {
    selectedRadio: function() {
      if (this.selectedRadio === "Uit") {
        this.drawHeatmap = false;
      } else {
        this.drawHeatmap = true;
      }
    },
    selectedBAGResult: function() {
      if (Object.keys(this.selectedBAGResult).length > 0) {
        if (
          this.selectedBAGResult["status"] === "Verblijfsobject in gebruik" ||
          this.selectedBAGResult["status"] === "Plaats aangewezen"
        ) {
          this.bagIsWoning = true;
        } else {
          this.bagIsWoning = false;
        }
      }
    }
  },
  methods: {
    // Small methods to update the data with component events
    // Maybe there's a more efficient way, but inline data setting seems ugly
    updateSelectedFilters: function(value) {
      this.selectedCategories = value;
    },
    updateSelectedRadio: function(value) {
      this.selectedRadio = value;
    },
    updateSelectedAddressCoordinates: function(value) {
      this.selectedAddressCoordinates = value;
    },
    updateSelectedAddress: function(value) {
      this.selectedAddress = value;
    },
    updateSelectedBAGResult: function(value) {
      this.selectedBAGResult = value;
    },
    updateSelectedBAGResultPand: function(value) {
      this.selectedBAGResultPand = value;
    },
    updateSelectedBAGID: function(value) {
      this.selectedBAGID = value;
    }
  },
  computed: {
    // Sort categories alphabetically
    sortedCats: function() {
      function compare(a, b) {
        if (a.category < b.category) return -1;
        if (a.category > b.category) return 1;
        return 0;
      }
      const categorySorted = this.locationCategories;
      return categorySorted.sort(compare);
    },
    filteredData: function() {
      // map selected values (categories) to array
      let selectedValues = this.selectedCategories.map(el => el.category);
      // filter data with selected categories, create array with possibly multiple arrays of objects
      let filteredDataArrays = selectedValues.map(el =>
        locationData.filter(element => element.cat === el)
      );
      // make sure filtered data is empty if no values are selected
      let filteredData = [];
      if (filteredDataArrays.length > 0) {
        // reduce into single array of objects
        filteredData = filteredDataArrays.reduce((result, current) => {
          return result.concat(current);
        });
        // add camelcase and distance to each object
        filteredData.forEach(el => {
          const start = {
            latitude: this.selectedAddressCoordinates[1],
            longitude: this.selectedAddressCoordinates[0]
          };
          const end = {
            latitude: el.lat,
            longitude: el.lon
          };
          // haversine formula calculates distance, add to objects
          el.distanceToSelectedAddress = haversine(start, end);
          // lookup camelcased category value in category object and put in filteredData
          el.camel = this.sortedCats.find(e => e.category === el.cat).camelName;
        });
        // filter out objects > 1km (or radius' current value)
        filteredData = filteredData.filter(
          el => el.distanceToSelectedAddress < this.radius
        );
        return filteredData;
      }
    },
    filteredHeatmapData: function() {
      const coordsjson = this.heatmapData;
      return coordsjson.map(el => [el.lat, el.lng]);
    }
  }
};
</script>
<style>
.selection-pane {
  background-color: whitesmoke;
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
