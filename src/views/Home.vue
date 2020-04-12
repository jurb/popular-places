<template>
  <div class="home" v-if="!loading">
    <div class="columns">
      <div class="column is-narrow selection-pane">
        <p class="top-info">
          Data ververst op {{ prettyDate }} <br />
          <a @click="reloadPage">Ververs pagina</a> |
          <a
            href="https://docs.google.com/document/d/1lUI3qSzNs3U2FufbgKe4jFW5Ww2baPGrAUcZXdBKFqw/edit?usp=sharing"
            target="_blank"
            >Over deze kaart</a
          >
          | <a @click="logOut">Log uit</a>
        </p>
        <places-table
          v-on:selected="setSelectedLocation"
          :selected-location="selectedLocation"
          title="Hotspots ⚠️"
          :data="
            getTableData({
              data: filteredData.filter(el => hotspots.includes(el.id)),
              filterProperty: 'types',
              filterValue: 'point_of_interest',
              sortBy: 'current_popularity',
              numberOfRows: 9999
            })
          "
        />
        <places-table
          v-on:selected="setSelectedLocation"
          :selected-location="selectedLocation"
          title="Alle plekken 🚨"
          :data="
            getTableData({
              data: filteredData,
              filterProperty: 'types',
              filterValue: 'point_of_interest',
              sortBy: 'current_popularity',
              numberOfRows: 9999
            })
          "
        />
        <places-table
          v-on:selected="setSelectedLocation"
          :selected-location="selectedLocation"
          title="Parken 🌳"
          :data="
            getTableData({
              data: filteredData,
              filterProperty: 'types',
              filterValue: 'park',
              sortBy: 'current_popularity',
              numberOfRows: 9999
            })
          "
        />
        <places-table
          v-on:selected="setSelectedLocation"
          :selected-location="selectedLocation"
          title="Winkels 🛒"
          :data="
            getTableData({
              data: filteredData,
              filterProperty: 'types',
              filterValue: 'store',
              sortBy: 'current_popularity',
              numberOfRows: 9999
            })
          "
        />
        <div class="field">
          <h2>Categorieën ({{ filteredData.length }} items)</h2>
          <p class="selectors">
            <a @click="selectedTypes = typeUniques">Selecteer alles</a> |
            <a @click="selectedTypes = []">Deselecteer alles</a>
          </p>
          <div
            v-for="type in typeUniques"
            v-bind:key="type.id"
            class="checkbox-wrapper"
          >
            <b-checkbox v-model="selectedTypes" :native-value="type"
              >{{ type }} ({{
                filteredData.filter(el => el.types.includes(type)).length
              }})
            </b-checkbox>
          </div>
        </div>
      </div>
      <div class="column ">
        <places-map
          :data="filteredData"
          :selected-location="selectedLocation"
        />
      </div>
    </div>
  </div>
</template>

<script>
import placesTable from "@/components/placesTable.vue";
import placesMap from "@/components/placesMap.vue";
import * as d3 from "d3";
import firebase from "firebase/app";
import "firebase/auth";

export default {
  name: "home",
  data() {
    return {
      data: [],
      loading: true,
      selectedTypes: [],
      selectedLocation: {},
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
        "ChIJ3yDhlXMJxkcRXFBf6b2GjQU"
      ],
      typesOfInterest: ["park", "store", "hardware_store", "supermarket"],
      daysOfWeek: [
        "zondag",
        "maandag",
        "dinsdag",
        "woensdag",
        "donderdag",
        "vrijdag",
        "zaterdag"
      ],
      months: [
        "jan",
        "feb",
        "maart",
        "april",
        "mei",
        "juni",
        "juli",
        "aug",
        "sep",
        "okt",
        "nov",
        "dec"
      ],
      timeStamp: ""
    };
  },
  components: {
    placesTable,
    placesMap
  },
  watch: {},
  methods: {
    logOut() {
      firebase.auth().signOut();
    },
    reloadPage: function() {
      window.location.assign("/");
    },
    setSelectedLocation: function(value) {
      this.selectedLocation = value;
    },
    getTableData: function(obj) {
      return obj.data
        .filter(el => el[obj.filterProperty].includes(obj.filterValue))
        .slice()
        .sort((a, b) => b[obj.sortBy] - a[obj.sortBy])
        .slice(0, obj.numberOfRows);
    }
  },
  created: function() {
    this.selectedTypes = this.typeUniques;
    // this.selectedTypes = ["supermarket"];
  },
  mounted: function() {
    const that = this;
    d3.json("/data/newest.json").then(function(data) {
      that.data = data["places"];
      that.timeStamp = new Date(data["timestamp"] * 1000);
      // console.log(that.timeStamp);
      that.selectedTypes = that.typeUniques;
      that.loading = false;
    });
  },
  computed: {
    // set first day of the week to monday
    dayNumber: function() {
      return this.timeStamp.getDay() - 1 === -1
        ? 6
        : this.timeStamp.getDay() - 1;
    },
    hour: function() {
      return this.timeStamp.getHours() < 10
        ? "0" + this.timeStamp.getHours()
        : this.timeStamp.getHours();
    },
    minute: function() {
      return this.timeStamp.getMinutes() < 10
        ? "0" + this.timeStamp.getMinutes()
        : this.timeStamp.getMinutes();
    },
    prettyDate: function() {
      return `${[
        this.daysOfWeek[this.timeStamp.getDay()],
        this.timeStamp.getDate(),
        this.months[this.timeStamp.getMonth()]
      ].join(" ")} ${this.hour}:${this.minute}`;
    },
    typeUniques() {
      const unwantedTypes = ["point_of_interest", "establishment"];
      const filterUnwantedTypes = el => !unwantedTypes.includes(el);
      const getUniques = arr => [...new Set(arr)];
      const types = arr => arr.flatMap(el => el.types);
      return getUniques(types(this.data)).filter(filterUnwantedTypes);
    },
    filteredData() {
      return this.data
        .filter(el =>
          this.selectedTypes.some(selectedCat => el.types.includes(selectedCat))
        )
        .map(el => ({
          ...el,
          usual_popularity: el.populartimes
            ? el.populartimes[this.dayNumber].data[this.hour]
            : null,
          difference: el.current_popularity
            ? el.current_popularity -
              el.populartimes[this.dayNumber].data[this.hour]
            : null
        }));
    }
  }
};
</script>
<style>
.selection-pane {
  background-color: whitesmoke;
  padding: 1rem;
}
.selectors {
  padding: 1rem;
  margin: 1rem;
}
.checkbox-wrapper {
  padding-left: 1rem;
}
.b-table {
  padding: 0rem;
}
.b-table:focus {
  outline: none;
}
p {
  font-size: 1em !important;
  margin: 1em !important;
  font-family: Avenir LT W01\ 85 Heavy, arial, sans-serif;
}
h2 {
  font-size: 1.3em !important;
  margin-top: 1em !important;
  margin-bottom: 0.5em !important;

  /* margin-bottom: 0.3em !important; */
  margin-left: 0.6em !important ;
  font-family: Avenir LT W01\ 85 Heavy, arial, sans-serif;
}
ul,
.block {
  margin-left: 0.8em !important ;
}
</style>
