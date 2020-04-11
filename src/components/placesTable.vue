<template>
  <div>
    <h2>{{ title }}</h2>
    <b-table
      :data="data"
      v-if="data.length"
      :selected.sync="selected"
      default-sort="current_popularity"
      default-sort-direction="desc"
      focusable
      detailed
      paginated
      sort-icon="^"
      per-page="10"
    >
      <template slot-scope="props">
        <b-table-column field="name" label="Naam" width="300">
          {{ props.row.name }}
        </b-table-column>
        <b-table-column
          field="current_popularity"
          label="Huidige pop. score"
          sortable
          width="40"
        >
          {{ props.row.current_popularity }}
        </b-table-column>
        <b-table-column
          field="usual_popularity"
          label="Gemiddelde pop. score op deze tijd"
          sortable
          width="40"
        >
          {{ props.row.usual_popularity }}
        </b-table-column>
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

<style lang="scss" scoped></style>
