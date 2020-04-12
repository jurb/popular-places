<template>
  <div>
    <h2>{{ title }}</h2>
    <b-table
      :data="data"
      v-if="data.length"
      :selected.sync="selected"
      default-sort="current_popularity"
      default-sort-direction="desc"
      detailed
      paginated
      sort-icon="^"
      per-page="10"
      narrowed
      :mobile-cards="false"
    >
      <template slot-scope="props">
        <b-table-column field="name" label="Naam" width="300">
          {{ props.row.name }}
        </b-table-column>
        <b-table-column
          field="current_popularity"
          label="Huidig"
          sortable
          width="40"
        >
          {{ props.row.current_popularity }}
        </b-table-column>
        <b-table-column
          field="usual_popularity"
          label="Normaal"
          sortable
          width="40"
        >
          {{ props.row.usual_popularity }}
        </b-table-column>
        <!-- <b-table-column field="difference" label="Verschil" sortable width="40">
          {{ props.row.difference }}
        </b-table-column> -->
      </template>
      <template slot="detail" slot-scope="props">
        <span>{{ props.row.address }}</span></template
      >
    </b-table>
  </div>
</template>

<script>
export default {
  props: ["data", "title", "selectedLocation"],
  data() {
    return {
      selected: {}
    };
  },
  watch: {
    selected: function(value) {
      this.$emit("selected", value);
    },
    selectedLocation: function(value) {
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
