<template>
  <div>
    <h2>{{ title }}</h2>
    <b-icon icon="menu-up" />
    <b-table :data="data" v-if="data.length">
      <template slot-scope="props">
        <b-table-column field="name" label="Naam" width="300">
          {{ props.row.name }}
        </b-table-column>
        <b-table-column
          field="current_popularity"
          label="Pop. score"
          sortable
          width="40"
        >
          {{ props.row.current_popularity }}
        </b-table-column>
        <b-table-column
          field="current_popularity"
          label="Stijging laatste uur (vb)"
          sortable
          width="40"
        >
          {{ props.row.current_popularity }}
        </b-table-column>
      </template>
    </b-table>
  </div>
</template>

<script>
export default {
  props: ["data", "title"],
};
</script>

<style lang="scss" scoped></style>
