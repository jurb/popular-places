<template>
  <div>
    <h2>{{title}}</h2>
    <table class="table">
      <tr>
        <th v-if="selectedBAGResult._stadsdeel.naam">Stadsdeel</th>
        <th v-if="selectedBAGResult._buurtcombinatie.naam">Wijk</th>
        <th v-if="selectedBAGResult.bouwlaag_toegang">Verd.</th>
        <th v-if="selectedBAGResultPand.results">Bouwjaar</th>
        <th v-if="selectedBAGResult.aantal_kamers">Kamers</th>
        <th v-if="selectedBAGResult.oppervlakte">m
          <sup>2</sup>
        </th>
      </tr>
      <tr>
        <td v-if="selectedBAGResult._stadsdeel.naam">{{ selectedBAGResult._stadsdeel.naam }}</td>
        <td v-if="selectedBAGResult._buurtcombinatie.naam">{{ selectedBAGResult._buurtcombinatie.naam }}</td>
        <td v-if="selectedBAGResult.bouwlaag_toegang">{{ selectedBAGResult.bouwlaag_toegang }}</td>
        <td v-if="selectedBAGResultPand.results">{{ selectedBAGResultPand.results[0].oorspronkelijk_bouwjaar }}</td>
        <td v-if="selectedBAGResult.aantal_kamers">{{ selectedBAGResult.aantal_kamers }}</td>
        <td v-if="selectedBAGResult.oppervlakte">{{ selectedBAGResult.oppervlakte }}</td>
      </tr>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {};
  },
  props: {
    selectedBAGResult: Object,
    selectedBAGResultPand: Object,
    title: String
  }
};
</script>

<style scoped>
.table {
  margin: 5px;
}
th {
  font-size: 0.7em;
}
td {
  font-size: 0.8em;
}
</style>
