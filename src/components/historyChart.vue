<template>
  <div id="container" class="svg-container" align="center">
    <!-- <h1>{{ title }}</h1> -->
    <svg :width="svgWidth" :height="svgHeight">
      <g class="axis">
        <text x=10 :y="yScale(50) + 3" fill="lightgrey">50</text>
        <line x1="25" :x2="this.svgWidth" :y1="yScale(50)" :y2="yScale(50)" stroke="lightgrey" stroke-dasharray="1" />
        <text v-if="dataMax > 105" x=10 :y="yScale(100) + 3" fill="lightgrey">100</text>
        <line v-if="dataMax > 105" x1="25" :x2="this.svgWidth" :y1="yScale(100)" :y2="yScale(100)" stroke="lightgrey" stroke-dasharray="1" />
        <text v-if="dataMax > 155" x=10 :y="yScale(150) + 3" fill="lightgrey">150</text>
        <line v-if="dataMax > 155" x1="25" :x2="this.svgWidth" :y1="yScale(150)" :y2="yScale(150)" stroke="lightgrey" stroke-dasharray="1" />
        <text v-if="dataMax > 205" x=10 :y="yScale(200) + 3" fill="lightgrey">200</text>
        <line v-if="dataMax > 205" x1="25" :x2="this.svgWidth" :y1="yScale(200)" :y2="yScale(200)" stroke="lightgrey" stroke-dasharray="1" />
          </g>
      <g>
        <rect
          v-for="(item, index) in dayData"
          class="bar-positive"
          :key="`bar-${index}`"
          :x="xScale(index)"
          :y="yScale(item)"
          rx="3"
          :width="xScale.bandwidth()"
          :height="
            svgHeight - yScale(item) - 20 > 0
              ? svgHeight - yScale(item) - 15
              : 0
          "
        ></rect>
        <text
          v-for="(item, index) in dayData"
          :key="`text-${index}`"
          :x="xScale(index) + xScale.bandwidth() / 2"
          :y="svgHeight"
        >
          <tspan v-if="ticks.includes(index)">{{ index }}</tspan>
        </text>
        <rect
          class="bar-current"
          rx="3"
          :x="xScale(currentMeasurement.hour)"
          :y="yScale(currentMeasurement.measurement)"
          :width="xScale.bandwidth()"
          :height="
            svgHeight - yScale(currentMeasurement.measurement) - 15 > 0
              ? svgHeight - yScale(currentMeasurement.measurement) - 15
              : 0
          "
        ></rect>
      </g>
    </svg>
  </div>
</template>

<script>
import { scaleLinear, scaleBand } from 'd3-scale';
import { max, min } from 'd3-array';
import { selectAll } from 'd3-selection';
import { transition } from 'd3-transition';

export default {
  name: 'BarChart',
  props: {
    title: String,
    dayData: Array,
    currentMeasurement: Object
  },
  mounted() {
    this.svgWidth = document.getElementById('container').offsetWidth * 0.75;
    this.AddResizeListener();
  },
  data: () => ({
    svgWidth: 0,
    ticks: [3, 6, 9, 12, 15, 18, 21]
  }),
  methods: {
    AddResizeListener() {
      window.addEventListener('resize', () => {
        this.$data.svgWidth =
          document.getElementById('container').offsetWidth * 0.75;
      });
    }
  },
  computed: {
    dataMax() {
      return max(
        [...this.dayData, this.currentMeasurement.measurement],
        d => d
      );
    },
    dataMin() {
      return min(this.dayData, d => d);
    },
    xScale() {
      return scaleBand()
        .rangeRound([0, this.svgWidth])
        .padding(0.1)
        .domain(this.dayData.map((d, index) => index));
    },
    yScale() {
      return scaleLinear()
        .rangeRound([this.svgHeight - 25, 0])
        // TODO: use better heuristic than min/max for y scale graphs
        .domain([0, this.dataMax < 60 ? 60 : this.dataMax]);
    },
    svgHeight() {
      // return this.svgWidth / 1.61803398875; // golden ratio
      return this.svgWidth / 4; // golden ratio
    }
  }
};
</script>

<style scoped>
.bar-positive {
  fill: steelblue;
  transition: r 0.2s ease-in-out;
  opacity: 0.8;
  border-radius: 3px 3px 0 0;
}
.bar-current {
  fill: hotpink;
  opacity: 0.5;
  transition: r 0.2s ease-in-out;
}

.bar-positive:hover {
  fill: hotpink;
}

.svg-container {
  display: inline-block;
  position: relative;
  width: 100%;
  padding-bottom: 1%;
  vertical-align: top;
  overflow: hidden;
}

text {
  text-anchor: middle;
  font-size: 0.675rem;
}
</style>
