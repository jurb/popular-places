<template>
  <div>
    <h2>{{ title }}</h2>
    <b-table
      :data="data"
      v-if="data.length"
      :selected.sync="selected"
      :default-sort="sortBy"
      default-sort-direction="desc"
      detailed
      paginated
      narrowed
      sort-icon="chevron-up"
      per-page="10"
      :mobile-cards="false"
    >
      <template slot-scope="props">
        <b-table-column
          field="properties.name"
          label="Naam"
          width="300"
          searchable
        >
          {{ props.row.properties.name }}
        </b-table-column>
        <b-table-column
          field="properties.current_popularity"
          label="Huidig"
          sortable
          width="40"
        >
          <template slot="header" slot-scope="{ column }">
            <b-tooltip
              label="Op dit uur gemeten score"
              position="is-bottom"
              dashed
            >
              {{ column.label }}
            </b-tooltip>
          </template>
          {{ props.row.properties.current_popularity }}
        </b-table-column>
        <b-table-column
          field="properties.avg_p"
          label="Normaal"
          sortable
          width="40"
        >
          <template slot="header" slot-scope="{ column }">
            <b-tooltip
              label="Gemiddelde drukte op deze tijd en dag"
              position="is-bottom"
              dashed
            >
              {{ column.label }}
            </b-tooltip>
          </template>
          {{ props.row.properties.avg_p }}
        </b-table-column>
        <b-table-column
          field="diff_current_average"
          label="Verschil"
          sortable
          width="40"
        >
          {{ props.row.diff_current_average }}
        </b-table-column>
        <b-table-column field="combinedType" label="Categorie" width="40">
          {{ props.row.combinedType.filter(el => el).join(', ') }}
        </b-table-column>
        <!-- <b-table-column field="difference" label="Verschil" sortable width="40">
          {{ props.row.difference }}
        </b-table-column> -->
      </template>
      <template slot="detail" slot-scope="props">
        <place-details
          v-on:place-updated="$emit('place-updated')"
          :id="props.row.id"
          :timestamp="timestamp"
        />
      </template>
    </b-table>
  </div>
</template>

<script>
import placeDetails from '@/components/placeDetails.vue';
export default {
  props: ['data', 'title', 'selectedLocation', 'sortBy', 'timestamp'],
  components: { placeDetails },
  data() {
    return {
      selected: {}
    };
  },
  watch: {
    selected: function(value) {
      this.$emit('selected', value);
    },
    selectedLocation: function() {
      this.selected = this.selectedLocation;
    }
  }
};
</script>

<style lang="scss">
.b-table .table th {
  font-weight: 600;
  // font-size: 0.7rem;
  hyphens: manual;
}
</style>
