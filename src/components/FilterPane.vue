<template>
  <div class="field">
    <h2>{{title}}</h2>
    <ul>
      <li v-for="cat in categories" v-bind:key="cat.zaak_id">
        <b-checkbox v-model="selected" :native-value="cat">{{ cat.category }}
        </b-checkbox>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selected: []
    };
  },
  props: {
    categories: Array,
    title: String
  },
  watch: {
    selected: function() {
      this.$emit("selected", this.selected);
    }
  }
};
</script>

<style scoped>
li {
  font-size: 1em;
  padding: 0.1em;
  margin-right: 60px;
}
</style>
