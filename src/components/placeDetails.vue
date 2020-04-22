<template>
  <div>
    <!-- <div>{{ currentMeasurement }}</div> -->
    <history-chart
      :day-data="dayData"
      :current-measurement="currentMeasurement"
      title="chart title"
    />
  </div>
</template>

<script>
import * as d3 from 'd3';
import { rollup, group, merge } from 'd3-array';
import historyChart from '@/components/historyChart.vue';

export default {
  props: ['id', 'timestamp'],
  components: { historyChart },
  data() {
    return { data: null, enhancedData: {} };
  },
  mounted: function(id) {
    const that = this;
    d3.json(`https://covid19.api.commondatafactory.nl/place/${this.id}`, {
      headers: new Headers({
        Authorization: `Basic ${btoa(
          `${process.env.VUE_APP_PLACES_API_USER}:${
            process.env.VUE_APP_PLACES_API_PASS
          }`
        )}`
      })
    }).then(function(data) {
      return (that.data = data);
    });
  },
  methods: {
    //     enhanceData: function() {
    //       const currentMeasurement = d3.max(this.data['measurements'], d => d);
    //       const measurementsDates = this.data['measurements'].map(el => ({
    //         date: new Date(el[0] * 1000),
    //         hour: new Date(el[0] * 1000).getHours(),
    //         day: new Date(el[0] * 1000).getDay(),
    //         measurement: el[1]
    //       }));
    //       return this.data
    //         ? {
    //             ...this.data,
    //             currentMeasurement: Object.assign({
    //               date: new Date(currentMeasurement[0] * 1000),
    //               hour: new Date(currentMeasurement[0] * 1000).getHours(),
    //               day: new Date(currentMeasurement[0] * 1000).getDay(),
    //               measurement: currentMeasurement[1]
    //             }),
    //             measurements: measurementsDates
    //           }
    //         : {};
    //     }
  },
  computed: {
    currentMeasurement: function() {
      const timestamp = () => d3.max(this.data['measurements'], d => d[0]);
      const date = () => new Date(timestamp() * 1000);
      return this.data
        ? {
            date: date(),
            day: date().getDay() - 1 === -1 ? 6 : date().getDay() - 1,
            hour: date().getHours(),
            measurement: this.data['current_popularity']
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
