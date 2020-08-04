<template>
  <div v-if="data">
    <div>
      Meting: {{ currentMeasurement.prettyDate }},
      {{ currentMeasurement.prettyHour }}:{{
        currentMeasurement.prettyMinute
      }}.<br />
      Adres: {{ data.address.slice(0, -32) }}<br />
      ID: {{ data.id }}
    </div>
    <history-chart
      :day-data="dayData"
      :current-measurement="currentMeasurement"
      title="chart title"
    />
    <div>
      <a @click="refreshPlaceData(id)">Ververs data</a> |
      <a @click="ignorePlace(id)">Verberg</a>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3';
import historyChart from '@/components/historyChart.vue';

export default {
  props: ['id', 'timestamp'],
  components: { historyChart },
  data() {
    return {
      data: null,
      enhancedData: {},
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
      ]
    };
  },
  mounted: function() {
    this.getPlaceData(this.id);
  },
  methods: {
    getPlaceData: function(id) {
      const that = this;
      d3.json(
        `https://covid19.api.commondatafactory.nl/place/${id}?timestamp=${Math.floor(
          this.timestamp / 1000
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
      ).then(function(data) {
        return (that.data = data);
      });
    },
    refreshPlaceData: function(id) {
      const that = this;
      d3.json(`https://covid19.api.commondatafactory.nl/scrape_place/${id}`, {
        headers: new Headers({
          Authorization: `Basic ${btoa(
            `${process.env.VUE_APP_PLACES_API_USER}:${
              process.env.VUE_APP_PLACES_API_PASS
            }`
          )}`
        })
      }).then(function(data) {
        that.getPlaceData(id);
        that.$emit('place-updated');
      });
    },
    ignorePlace: function(id) {
      const that = this;
      d3.json(`https://covid19.api.commondatafactory.nl/ignore_place/${id}`, {
        method: 'POST',
        headers: new Headers({
          Authorization: `Basic ${btoa(
            `${process.env.VUE_APP_PLACES_API_USER}:${
              process.env.VUE_APP_PLACES_API_PASS
            }`
          )}`
        })
      }).then(function(data) {
        that.$emit('place-updated');
      });
    }
  },
  computed: {
    // TODO: show the right hour when stepping through time
    currentMeasurement: function() {
      const timestamp = () => d3.max(this.data['measurements'], d => d[0]);
      const date = () => new Date(timestamp() * 1000);
      // const date = () => new Date(this.timestamp);
      return this.data
        ? {
            date: date(),
            day: date().getDay() - 1 === -1 ? 6 : date().getDay() - 1,
            hour: date().getHours(),
            measurement: this.data['current_popularity'],
            prettyDate: `${[
              this.daysOfWeek[date().getDay()],
              date().getDate(),
              this.months[date().getMonth()]
            ].join(' ')}`,
            prettyHour:
              date().getHours() < 10
                ? '0' + date().getHours()
                : date().getHours(),
            prettyMinute:
              date().getMinutes() < 10
                ? '0' + date().getMinutes()
                : date().getMinutes()
          }
        : {};
    },
    dayData: function() {
      return this.data
        ? this.data['measured_popularity'][this.currentMeasurement.day]['data']
        : [];
    }
  }
};
</script>

<style lang="scss" scoped></style>
