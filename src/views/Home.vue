<template>
  <div>
    <div class="columns">
      <div class="column is-half is-narrow is-gapless selection-pane">
        <div v-if="!render && loading">Data ophalen van de API...</div>
        <div v-if="!render && loading && errorCount > 24">
          De popular places API lijkt down, er komt niks terug van
          <a href="https://covid19.api.commondatafactory.nl/popularplaces"
            >https://covid19.api.commondatafactory.nl/popularplaces</a
          >. Neem contact op met de beheerder.
        </div>
      </div>
    </div>
    <div class="home" v-if="render">
      <div class="columns">
        <div class="column is-half is-narrow is-gapless selection-pane">
          <div class="level is-mobile">
            <div class="level-left">
              <div class="level-item">
                <p v-if="errorCount > 24">
                  The places API seems to be down. Please
                  <a @click="reloadPage">reload the page</a> to try again.
                </p>
                <p class="top-bar">
                  Data rond
                  <b-dropdown aria-role="list">
                    <a slot="trigger" slot-scope="{ active }">
                      {{ prettyDate }} </a
                    ><b-dropdown-item custom inline>
                      <b-datetimepicker
                        v-model="datetimePicker"
                        inline
                        :focused-date="new Date()"
                        :datepicker="{
                          firstDayOfWeek: 1,
                          dayNames: ['Zo', 'Ma', 'Di', 'Wo', 'Do', 'Vr', 'Za']
                        }"
                        :max-datetime="new Date()"
                        :min-datetime="new Date('2020-04-12')"
                      ></b-datetimepicker></b-dropdown-item
                  ></b-dropdown>
                  &nbsp;<b-button
                    @click="setData(timestamp - 3600000, 'left')"
                    size="is-small"
                    icon-right="chevron-left"
                    :loading="loading"
                  ></b-button
                  ><span> {{ prettyHour }}:{{ prettyMinute }} </span>
                  <b-button
                    v-if="
                      Math.floor(timestamp / 1100) !==
                        Math.floor(initialTimestamp / 1100)
                    "
                    @click="setData(timestamp + 3600000, 'right')"
                    size="is-small"
                    icon-right="chevron-right"
                    :loading="loading"
                  ></b-button>
                </p>
              </div>
            </div>
            <div class="level-right">
              <div class="level-item">
                <p>
                  <span id="weather" v-if="weatherResponse.current"
                    >&nbsp;<img
                      class="weather-block"
                      :src="
                        `https://openweathermap.org/img/wn/${
                          weatherResponse.current.weather[0].icon
                        }@2x.png`
                      "
                      width="50"
                    />
                    <span style="vertical-align: -0.6rem">
                      {{ Math.round(weatherResponse.current.temp) }} °C</span
                    ></span
                  >
                </p>
              </div>
            </div>
          </div>

          <b-tabs v-model="activeTab" size="is-medium" :animated="false">
            <b-field
              grouped
              group-multiline
              class="checkbox-field"
              v-if="selectedTypes"
            >
              <b-checkbox
                v-for="type in combinedTypeUniques"
                v-bind:key="type.id"
                v-model="selectedTypes"
                :native-value="type"
                outlined
                >{{ type }} ({{
                  filteredData.filter(el => el.combinedType.includes(type))
                    .length
                }})
              </b-checkbox>
            </b-field>
            <b-tab-item :label="`Alle plekken (${filteredData.length} items)`">
              <places-table
                v-on:selected="setSelectedLocation"
                v-on:place-updated="setData(+new Date())"
                :selected-location="selectedLocation"
                title=""
                :timestamp="timestamp"
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
            </b-tab-item>
            <b-tab-item label="Hotspots ⚠️">
              <group-table
                v-if="groupsData.length > 0"
                :data="groupsData"
                title=""
                v-on:selected="setSelectedLocation"
                :selected-location="selectedLocation"
              />
            </b-tab-item>
          </b-tabs>
          <ul class="menu">
            <li>
              <a
                @click="
                  initialTimestamp = +new Date();
                  setData(+new Date());
                "
                >Nieuwste data</a
              >
            </li>
            <li>
              <a
                href="https://docs.google.com/document/d/1lUI3qSzNs3U2FufbgKe4jFW5Ww2baPGrAUcZXdBKFqw/edit?usp=sharing"
                target="_blank"
                >Over deze kaart <b-icon icon="open-in-new" size="is-small"
              /></a>
            </li>
            <li>
              <b-collapse
                :open="false"
                position="is-top"
                aria-id="contentIdForA11y1"
              >
                <a
                  slot="trigger"
                  slot-scope="props"
                  aria-controls="contentIdForA11y1"
                >
                  Locatie toevoegen
                  <b-icon
                    size="is-small"
                    :icon="!props.open ? 'chevron-down' : 'chevron-up'"
                  ></b-icon>
                </a>
                <div class="callout">
                  <p
                    v-html="
                      addPlaceResponse === 'Error'
                        ? 'Dit is geen geldige place ID'
                        : addPlaceResponse
                    "
                  ></p>
                  <p>
                    <b-input placeholder="Place ID" v-model="addPlaceInput">
                    </b-input>
                  </p>
                  <p>
                    <button
                      class="button is-primary"
                      @click="addPlace(addPlaceInput)"
                    >
                      Voeg toe
                    </button>
                  </p>
                </div>
              </b-collapse>
            </li>
            <li>
              <b-collapse
                :open="false"
                position="is-top"
                aria-id="contentIdForA11y1"
              >
                <a
                  slot="trigger"
                  slot-scope="props"
                  aria-controls="contentIdForA11y1"
                >
                  Verborgen locaties beheren
                  <b-icon
                    size="is-small"
                    :icon="!props.open ? 'chevron-down' : 'chevron-up'"
                  ></b-icon>
                </a>
                <div class="callout content">
                  <ul v-if="ignored.ignored">
                    <li v-for="place in ignored.ignored" v-bind:key="place">
                      {{ place }} -
                      <a @click="unIgnorePlace(place)">laat weer zien</a>
                    </li>
                  </ul>
                  <p class="is-size-7">
                    Naam en adres van verborgen locaties volgt binnenkort.
                  </p>
                  <!-- <p>Sortering is van nieuw naar oud.</p> -->
                </div>
              </b-collapse>
            </li>

            <li>
              <a href="https://github.com/jurb/popular-places" target="_blank"
                >Github repo</a
              >
            </li>
            <li><a @click="logOut">Log uit</a></li>
          </ul>
        </div>
        <div class="column">
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
      ignored: {},
      initialLoad: true,
      errorCount: 0,
      groups: [],
      activeTab: 0,
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
      datetimePicker: new Date(),
      date: '',
      addPlaceInput: null,
      addPlaceResponse:
        'Kijk op <a href="https://maps.google.com" target="blank">Google Maps</a> of een plek een live meting heeft (roze balkje in de grafiek), en zoek <a href="https://developers.google.com/places/place-id", target="_blank">hier</a> de bijbehorende Place ID op.',
      weatherResponse: {}
    };
  },
  components: {
    placesTable,
    groupTable,
    placesMap
  },
  watch: {
    datetimePicker: function() {
      this.setData(+this.datetimePicker);
    }
  },
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
          that.dataInBounds = that.data = data['features'].map(el => ({
            ...el,
            properties: {
              ...el.properties,
              diff_current_average:
                el.properties.current_popularity - el.properties.avg_p
            }
          }));
          that.timestamp = timestamp;
          that.date = new Date(timestamp);
          that.render = true;
          that.loading = false;
          that.errorCount = 0;
        })
        .then(function(data) {
          d3.json(
            `https://api.openweathermap.org/data/2.5/onecall/timemachine?lat=52.3667&lon=4.8945&dt=${Math.floor(
              timestamp / 1000
            )}&appid=${
              process.env.VUE_APP_OPENWEATHERMAP_API
            }&units=metric&lang=nl`
          )
            .then(function(data) {
              that.weatherResponse = data;
            })
            .catch(function(error) {
              console.log(error);
              that.weatherResponse.current = null;
            });
        })
        .then(function(data) {
          d3.json(`https://covid19.api.commondatafactory.nl/ignored`, {
            headers: new Headers({
              Authorization: `Basic ${btoa(
                `${process.env.VUE_APP_PLACES_API_USER}:${
                  process.env.VUE_APP_PLACES_API_PASS
                }`
              )}`
            })
          })
            .then(function(data) {
              that.ignored = data;
            })
            .catch(function(error) {
              console.log(error);
            });
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
      return data
        .map(el => ({
          ...el,
          combinedType: [
            ...new Set(el.properties.types.map(el => this.combinedTypes[el]))
          ]
        }))
        .filter(el =>
          this.selectedTypes.some(selectedCat =>
            el.combinedType.includes(selectedCat)
          )
        );
    },
    addPlace: function(id) {
      const that = this;
      d3.json(`https://covid19.api.commondatafactory.nl/scrape_place/${id}`, {
        headers: new Headers({
          Authorization: `Basic ${btoa(
            `${process.env.VUE_APP_PLACES_API_USER}:${
              process.env.VUE_APP_PLACES_API_PASS
            }`
          )}`
        })
      })
        .then(function(data) {
          that.addPlaceResponse = data;
        })
        .then(function() {
          that.setData(+new Date());
          that.addPlaceInput = null;
        })
        .catch(function(error) {
          that.addPlaceResponse = 'Error';
        });
    },
    unIgnorePlace: function(id) {
      const that = this;
      d3.json(
        `https://covid19.api.commondatafactory.nl/ignore_place/${id}?ignore=false`,
        {
          method: 'POST',
          headers: new Headers({
            Authorization: `Basic ${btoa(
              `${process.env.VUE_APP_PLACES_API_USER}:${
                process.env.VUE_APP_PLACES_API_PASS
              }`
            )}`
          })
        }
      ).then(function(data) {
        that.setData(+new Date());
      });
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
      // select all types on mount
      that.selectedTypes = [...new Set(data.map(el => el.combinedType))];
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
  font-size: 1.25em !important;
  margin: 1em !important;
  font-family: Avenir LT W01\ 85 Heavy, arial, sans-serif;
}
.menu {
  font-family: Avenir LT W01\ 85 Heavy, arial, sans-serif;
  font-size: 1.25em !important;
  margin-left: 1rem;
}

h2 {
  font-size: 1.3em !important;
  margin-top: 1em !important;
  margin-bottom: 0.5em !important;

  /* margin-bottom: 0.3em !important; */
  margin-left: 0.6em !important ;
  font-family: Avenir LT W01\ 85 Heavy, arial, sans-serif;
}

.block {
  margin-left: 0.8em !important ;
}
.input {
  margin: 0;
}
.callout {
  padding: 0.2rem;
  margin: 0.2rem;
  background-color: gainsboro;
  font-size: 1rem !important;
}
.dropdown-content {
  background-color: #00000000;
  border-radius: 4px;
  -webkit-box-shadow: 0 2px 3px rgba(10, 10, 10, 0.1),
    0 0 0 1px rgba(10, 10, 10, 0.1);
  box-shadow: 0 2px 3px rgba(10, 10, 10, 0), 0 0 0 1px rgba(10, 10, 10, 0);
  padding-bottom: 0.5rem;
  padding-top: 0.5rem;
}
.checkbox-field {
  margin: 1rem 0 0.25rem 1rem !important;
}
.b-tabs .tab-content {
  padding: 0rem;
}
.top-bar {
  vertical-align: text-top;
}
.weather-block {
  /* background-color: gray; */
  filter: invert(10%);
}
</style>
