<template>
  <div>
    <l-map
      class="map"
      :zoom="map.zoom"
      :center="map.center"
      :options="{ preferCanvas: true }"
      ref="map"
      @update:bounds="boundsUpdated"
    >
      <l-control position="bottomright">
        <button class="button" @click="scrollToTop">^</button>
      </l-control>
      <l-tile-layer
        :url="map.url"
        :attribution="map.attribution"
      ></l-tile-layer>
      <l-circle
        v-for="point in data"
        v-bind:key="point.id"
        :lat-lng="point.geometry.coordinates.slice().reverse()"
        :radius="popularity2radius(point.properties.current_popularity)"
        :color="
          (Array.isArray(selectedLocation.id)
            ? selectedLocation.id
            : [selectedLocation.id]
          ).includes(point.id)
            ? '#f03'
            : 'blue'
        "
        :opacity="0.5"
      >
        <l-tooltip>{{ point.properties.name }} </l-tooltip
        ><l-popup>
          {{ point.properties.name }} <br />
          Adres: {{ point.properties.address.split(',')[0] }} <br />

          Huidige pop. score: {{ point.properties.current_popularity }} <br />
          Normale pop. score: {{ point.properties.avg_p }} <br />
          Laatst ververst op:
          {{
            `${new Date(point.properties.scraped_at * 1000).getDate()} ${
              months[new Date(point.properties.scraped_at * 1000).getMonth()]
            } ${new Date(point.properties.scraped_at * 1000).getFullYear()}
            ${
              new Date(point.properties.scraped_at * 1000).getHours() < 10
                ? '0' + new Date(point.properties.scraped_at * 1000).getHours()
                : new Date(point.properties.scraped_at * 1000).getHours()
            }:${
              new Date(point.properties.scraped_at * 1000).getMinutes() < 10
                ? '0' +
                  new Date(point.properties.scraped_at * 1000).getMinutes()
                : new Date(point.properties.scraped_at * 1000).getMinutes()
            }`
          }}
          <br />
          <a
            :href="`https://www.google.com/maps?q=${point.properties.name}`"
            target="_blank"
            s
            >Google Maps</a
          ></l-popup
        ></l-circle
      >
    </l-map>
    <p><em>Hoe groter de cirkel, hoe drukker de plek op dit moment is.</em></p>
  </div>
</template>

<script>
import L from 'leaflet';
import {
  LMap,
  LTileLayer,
  LMarker,
  LCircleMarker,
  LCircle,
  LPopup,
  LControlZoom,
  LTooltip,
  LControl
} from 'vue2-leaflet';
import 'leaflet/dist/leaflet.css';
import * as d3 from 'd3';

export default {
  name: 'kaart',
  props: ['data', 'selectedLocation'],
  data() {
    return {
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
      map: {
        zoom: 11,
        center: L.latLng(52.3702, 4.8952),
        url:
          'https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png',
        attribution: 'CC-BY-4.0 Gemeente Amsterdam'
      },
      bounds: null,
      localData: this.data
    };
  },
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LCircleMarker,
    LCircle,
    LPopup,
    LControlZoom,
    LTooltip,
    LControl
  },
  watch: {},
  methods: {
    scrollToTop() {
      window.scrollTo(0, 0);
    },
    boundsUpdated() {
      const dataInBounds = this.data.filter(el =>
        this.$refs.map.mapObject
          .getBounds()
          .contains(
            L.latLng(el.geometry.coordinates[1], el.geometry.coordinates[0])
          )
      );
      this.$emit('data-in-bounds', dataInBounds);
    }
  },
  computed: {
    popularity2radius: function() {
      return (
        d3
          .scaleSqrt()
          // .domain(d3.extent(this.localData, d => d.difference))
          // .domain(d3.extent(this.localData, d => d.current_popularity))
          // .domain([0, d3.max(this.localData, d => d.current_popularity)])
          .domain([0, 200])
          .range([0, 200])
      );
    }
  }
};
</script>
<style scoped>
.map {
  height: 600px !important;
}
@media (min-width: 768px) {
  .map {
    height: 995px !important;
  }
  .button {
    display: none !important;
  }
}
</style>
