<template>
  <div>
    <p v-if="errorCount > 24">
      The places API seems to be down. Please
      <a @click="reloadPage">reload the page</a> to try again.
    </p>
    <div class="home" v-if="render">
      <div class="columns">
        <div class="column is-half is-narrow selection-pane">
          <!-- <history-chart :data="data" /> -->
          <p class="top-info">
            <a
              @click="
                initialTimestamp = +new Date();
                setData(+new Date());
              "
              >Nieuwste data</a
            >
            |
            <a
              href="https://docs.google.com/document/d/1lUI3qSzNs3U2FufbgKe4jFW5Ww2baPGrAUcZXdBKFqw/edit?usp=sharing"
              target="_blank"
              >Over deze kaart</a
            >
            | <a @click="logOut">Log uit</a>
          </p>
          <p>
            Data rond {{ prettyDate }} <br />
            <b-button
              @click="setData(timestamp - 3600000, 'left')"
              size=""
              icon-right="chevron-left"
              :loading="loading"
            ></b-button
            ><span class="is-size-4">
              {{ prettyHour }}:{{ prettyMinute }}
            </span>
            <b-button
              v-if="
                Math.floor(timestamp / 1000) !==
                  Math.floor(initialTimestamp / 1000)
              "
              @click="setData(timestamp + 3600000, 'right')"
              size=""
              icon-right="chevron-right"
              :loading="loading"
            ></b-button>
          </p>
          <h2>Categorieën ({{ filteredData.length }} items)</h2>
          <b-field style="margin-left: 0.6rem;" grouped group-multiline>
            <b-checkbox-button
              v-for="type in combinedTypeUniques"
              v-bind:key="type.id"
              v-model="selectedTypes"
              :native-value="type"
              >{{ type }} ({{
                filteredData.filter(el => el.combinedType.includes(type))
                  .length
              }})
            </b-checkbox-button></b-field
          >
          <group-table
            v-if="groupsData.length > 0"
            :data="groupsData"
            title="Hotspots ⚠️"
            v-on:selected="setSelectedLocation"
            :selected-location="selectedLocation"
          />
          <places-table
            v-on:selected="setSelectedLocation"
            :selected-location="selectedLocation"
            title="Drukte plekken in beeld op kaart 🗺"
            sortBy="properties.current_popularity"
            :data="
              getTableData({
                data: filteredDataInBounds,
                filterProperty: 'types',
                filterValue: 'point_of_interest',
                sortBy: 'current_popularity',
                numberOfRows: 9999
              })
            "
            v-if="
              getTableData({
                data: filteredDataInBounds,
                filterProperty: 'types',
                filterValue: 'point_of_interest',
                sortBy: 'current_popularity',
                numberOfRows: 9999
              }).length > 0
            "
          />
          <places-table
            v-on:selected="setSelectedLocation"
            :selected-location="selectedLocation"
            title="Drukte parken 🌳"
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
            v-if="
              getTableData({
                data: filteredData,
                filterProperty: 'types',
                filterValue: 'park',
                sortBy: 'current_popularity',
                numberOfRows: 9999
              }).length > 0
            "
          />
          <places-table
            v-on:selected="setSelectedLocation"
            :selected-location="selectedLocation"
            title="Drukte winkels 🛒"
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
            v-if="
              getTableData({
                data: filteredData,
                filterProperty: 'types',
                filterValue: 'store',
                sortBy: 'current_popularity',
                numberOfRows: 9999
              }).length > 0
            "
          />
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
  </div>
</template>

<script>
import placesTable from '@/components/placesTable.vue';
import groupTable from '@/components/groupTable.vue';
import placesMap from '@/components/placesMap.vue';
import * as d3 from 'd3';
import { rollup, group, merge } from 'd3-array';
import firebase from 'firebase/app';
import 'firebase/auth';

export default {
  name: 'home',
  data() {
    return {
      json: {},
      data: [],
      dataInBounds: [],
      render: false,
      loading: true,
      selectedDatetime: null,
      selectedTypes: [],
      selectedCombinedTypes: [],
      selectedLocation: {},
      initialLoad: true,
      errorCount: 0,
      groups: [],
      combinedTypes: [],
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
      initialTimestamp: +new Date(),
      timestamp: +new Date(),
      date: ''
    };
  },
  components: {
    placesTable,
    groupTable,
    placesMap
  },
  watch: {},
  methods: {
    getInitialTimestamp: function() {
      // TODO: get timestamp from first api call instead of local system
    },
    setData: function(timestamp = +new Date(), direction = 'none') {
      const that = this;
      that.loading = true;
      d3.json(
        `https://covid19.api.commondatafactory.nl/popularplaces?timestamp=${Math.floor(
          timestamp / 1000
        )}`,
        {
          headers: new Headers({
            Authorization: `Basic ${btoa(
              `${process.env.VUE_APP_PLACES_API_USER}:${
                process.env.VUE_APP_PLACES_API_PASS
              }`
            )}`
          })
        }
      )
        .then(function(data) {
          that.dataInBounds = that.data = data['features'];
          that.timestamp = timestamp;
          that.date = new Date(timestamp);
          // load unique types in selectedTypes filter array on first load
          !that.render ? (that.selectedTypes = that.combinedTypeUniques) : '';
          that.render = true;
          that.loading = false;
          that.errorCount = 0;
        })
        .catch(function(error) {
          ++that.errorCount;
          if (that.errorCount > 24) {
            return;
          } else direction === 'left' ? that.setData(timestamp - 3600000, 'left') : direction === 'right' ? that.setData(timestamp + 3600000, 'right') : that.setData(timestamp - 3600000, 'left');
        });
    },
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
      this.dataInBounds = value;
    },
    getTableData: function(obj) {
      return obj.data
        .filter(el =>
          el.properties[obj.filterProperty].includes(obj.filterValue)
        )
        .slice() // don't mutate original array
        .sort((a, b) => b[obj.sortBy] - a[obj.sortBy])
        .slice(0, obj.numberOfRows);
    },
    filterData: function(data) {
      return (
        data
          .map(el => ({
            ...el,
            diff_current_average:
              el.properties.current_popularity - el.properties.avg_p,
            combinedType: [
              ...new Set(el.properties.types.map(el => this.combinedTypes[el]))
            ]
          }))
          // .filter(el =>
          //   this.selectedTypes.some(selectedCat =>
          //     el.properties.types.includes(selectedCat)
          //   )
          // )
          .filter(el =>
            this.selectedTypes.some(selectedCat =>
              el.combinedType.includes(selectedCat)
            )
          )
      );
    }
  },
  mounted: function() {
    const that = this;
    d3.tsv('data/groups.tsv').then(function(data) {
      that.groups = data;
    });
    d3.tsv('data/combinedtypes.tsv').then(function(data) {
      that.combinedTypes = Object.assign(
        ...data.flatMap(el => ({ [el.type]: el.combinedType }))
      );
    });
    this.setData();
  },
  computed: {
    // set first day of the week to monday
    dayNumber: function() {
      return this.date.getDay() - 1 === -1 ? 6 : this.date.getDay() - 1;
    },
    hour: function() {
      return this.date.getHours();
    },
    prettyHour: function() {
      return this.date.getHours() < 10
        ? '0' + this.date.getHours()
        : this.date.getHours();
    },
    minute: function() {
      return this.date.getMinutes();
    },
    prettyMinute: function() {
      return this.date.getMinutes() < 10
        ? '0' + this.date.getMinutes()
        : this.date.getMinutes();
    },
    prettyDate: function() {
      return `${[
        this.daysOfWeek[this.date.getDay()],
        this.date.getDate(),
        this.months[this.date.getMonth()]
      ].join(' ')}`;
    },
    typeUniques() {
      const unwantedTypes = [
        'point_of_interest',
        'establishment',
        'supermarket',
        'food'
      ];
      const filterUnwantedTypes = el => !unwantedTypes.includes(el);
      const getUniques = arr => [...new Set(arr)];
      const types = arr => arr.flatMap(el => el.properties.types);
      return getUniques(types(this.data)).filter(filterUnwantedTypes);
    },
    combinedTypeUniques() {
      return [...new Set(Object.values(this.combinedTypes))];
    },
    filteredData() {
      return this.filterData(this.data);
    },
    filteredDataInBounds() {
      return this.filterData(this.dataInBounds);
    },
    groupsData() {
      // return Array.from(group(this.groups, el => el.group));
      return Array.from(group(this.groups, el => el.group))
        .map(el => ({
          group: el[0],
          places: this.filteredData.filter(d =>
            el[1].map(el => el.id).includes(d.id)
          )
        }))
        .filter(el => el.places.length > 0)
        .map(el => ({
          ...el,
          avg_current_popularity: Math.floor(
            d3.mean(el.places.map(d => d.properties.current_popularity))
          ),
          avg_avg_p: Math.floor(d3.mean(el.places.map(d => d.properties.avg_p)))
        }))
        .map(el => ({
          ...el,
          diff_current_average: el.avg_avg_p
            ? el.avg_current_popularity - el.avg_avg_p
            : null,
          id: el.places.map(el => el.id)
        }));

      // return Array.from(
      //   group(this.data.filter(d => d.group.length > 0), el => el.group)
      // ).map(el => ({ group: el[0], places: el[1] }));
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
