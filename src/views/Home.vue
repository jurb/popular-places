<template>
  <div class="home" v-if="!loading">
    <div class="columns">
      <div class="column is-half is-narrow selection-pane">
        <!-- <history-chart :data="data" /> -->
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
          title="Huidige drukte alle plekken 🚨"
          sortBy="properties.current_popularity"
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
          sortBy="properties.current_popularity"
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
          sortBy="properties.current_popularity"
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
                filteredData.filter(el => el.properties.types.includes(type))
                  .length
              }})
            </b-checkbox>
          </div>
        </div>
      </div>
      <div class="column ">
        <places-map
          v-on:data-in-bounds="setDataInBounds"
          :data="filteredData"
          :selected-location="selectedLocation"
        />
      </div>
    </div>
  </div>
</template>

<script>
import placesTable from '@/components/placesTable.vue';
import placesMap from '@/components/placesMap.vue';
import * as d3 from 'd3';
import firebase from 'firebase/app';
import 'firebase/auth';

export default {
  name: 'home',
  data() {
    return {
      data: [],
      loading: true,
      selectedTypes: [],
      selectedLocation: {},
      typesOfInterest: ['park', 'store', 'hardware_store', 'supermarket'],
      daysOfWeek: [
        'zondag',
        'maandag',
        'dinsdag',
        'woensdag',
        'donderdag',
        'vrijdag',
        'zaterdag'
      ],
      months: [
        'jan',
        'feb',
        'maart',
        'april',
        'mei',
        'juni',
        'juli',
        'aug',
        'sep',
        'okt',
        'nov',
        'dec'
      ],
      timestamp: ''
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
      window.location.assign('/');
    },
    setSelectedLocation: function(value) {
      this.selectedLocation = value;
    },
    setDataInBounds: function(value) {
      this.data = value;
    },
    getTableData: function(obj) {
      return obj.data
        .filter(el =>
          el.properties[obj.filterProperty].includes(obj.filterValue)
        )
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
    d3.json('https://covid19.api.commondatafactory.nl/popularplaces', {
      headers: new Headers({
        Authorization: `Basic ${btoa(
          `${process.env.VUE_APP_PLACES_API_USER}:${
            process.env.VUE_APP_PLACES_API_PASS
          }`
        )}`
      })
    }).then(function(data) {
      that.data = data['features'];
      that.timestamp = new Date(data['scraped_at'] * 1000);
      // console.log(that.timestamp);
      that.selectedTypes = that.typeUniques;
      that.loading = false;
    });
  },
  computed: {
    // set first day of the week to monday
    dayNumber: function() {
      return this.timestamp.getDay() - 1 === -1
        ? 6
        : this.timestamp.getDay() - 1;
    },
    hour: function() {
      return this.timestamp.getHours();
    },
    prettyHour: function() {
      return this.timestamp.getHours() < 10
        ? '0' + this.timestamp.getHours()
        : this.timestamp.getHours();
    },
    minute: function() {
      return this.timestamp.getMinutes();
    },
    prettyMinute: function() {
      return this.timestamp.getMinutes() < 10
        ? '0' + this.timestamp.getMinutes()
        : this.timestamp.getMinutes();
    },
    prettyDate: function() {
      return `${[
        this.daysOfWeek[this.timestamp.getDay()],
        this.timestamp.getDate(),
        this.months[this.timestamp.getMonth()]
      ].join(' ')} ${this.prettyHour}:${this.prettyMinute}`;
    },
    typeUniques() {
      const unwantedTypes = ['point_of_interest', 'establishment'];
      const filterUnwantedTypes = el => !unwantedTypes.includes(el);
      const getUniques = arr => [...new Set(arr)];
      const types = arr => arr.flatMap(el => el.properties.types);
      return getUniques(types(this.data)).filter(filterUnwantedTypes);
    },
    filteredData() {
      return this.data
        .filter(el =>
          this.selectedTypes.some(selectedCat =>
            el.properties.types.includes(selectedCat)
          )
        )
        .map(el => ({
          ...el,
          diff_current_average:
            el.properties.current_popularity - el.properties.avg_p
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
