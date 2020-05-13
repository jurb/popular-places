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
      <LGeoJson
        :geojson="veiligheidsregio"
        :options="veiligheidgeojsonoptions"
      />
      <LGeoJson :geojson="gebieden" :options="gebiedengeojsonoptions" />

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
            : popularity2color(point.properties.current_popularity)
        "
        :fillColor="popularity2color(point.properties.current_popularity)"
        :fillOpacity="0.8"
        :opacity="0.8"
      >
        <l-tooltip>{{ point.properties.name }} </l-tooltip
        ><l-popup>
          {{ point.properties.name }} <br />
          Adres: {{ point.properties.address.split(',')[0] }} <br />

          Huidige pop. score: {{ point.properties.current_popularity }} <br />
          Normale pop. score: {{ point.properties.avg_p }} <br />
          Data gemeten op:
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
          Categorie: {{ point.combinedType.filter(el => el).join(',') }} <br />
          <a
            :href="`https://www.google.com/maps?q=${point.properties.name}`"
            target="_blank"
            s
            >Google Maps</a
          ></l-popup
        ></l-circle
      >
    </l-map>
    <p>
      <em
        >Hoe groter en donkerder de cirkel, hoe drukker de plek op dit moment
        is.</em
      >
    </p>
  </div>
</template>

<script>
import L from 'leaflet';
import veiligheidsregio from '../../public/data/veiligheidsegio_amsterdam_amstelland.json';
import gebieden from '../../public/data/gebieden.json';

import {
  LMap,
  LTileLayer,
  LLayerGroup,
  LMarker,
  LCircleMarker,
  LCircle,
  LPopup,
  LControlZoom,
  LTooltip,
  LGeoJson,
  LControl
} from 'vue2-leaflet';
import 'leaflet/dist/leaflet.css';
import * as d3 from 'd3';

export default {
  name: 'kaart',
  props: ['data', 'selectedLocation'],
  data() {
    return {
      popupInstance: null,
      veiligheidsregio: veiligheidsregio,
      gebieden: gebieden,
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
      localData: this.data,
      gebiedengeojsonoptions: {
        style: {
          color: '#000',
          weight: 1,
          opacity: 0.2,
          fill: false
        }
      },
      veiligheidgeojsonoptions: {
        style: {
          color: '#8b0000',
          weight: 1,
          opacity: 0.5,
          fill: false
        }
      }
    };
  },
  components: {
    LMap,
    LTileLayer,
    LLayerGroup,
    LMarker,
    LCircleMarker,
    LCircle,
    LPopup,
    LControlZoom,
    LTooltip,
    LGeoJson,
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
      console.log(this.popularity2color(423));
    }
  },
  computed: {
    popularity2radius: function() {
      return (
        d3
          .scaleSqrt()
          // .domain(d3.extent(this.localData, d => d.difference))
          // .domain(
          //   d3.extent(this.localData, d => d.properties.current_popularity)
          // )
          // .domain([0, d3.max(this.localData, d => d.current_popularity)])
          .domain([0, 400])
          .range([0, 300])
      );
    },
    popularity2color: function() {
      return d3
        .scaleSequential()
        .domain([0, 200])
        .interpolator(d3.interpolateOrRd);
    },
    popularity2opacity: function() {
      return d3
        .scaleLinear()
        .domain([0, 400])
        .range([0.1, 1]);
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
