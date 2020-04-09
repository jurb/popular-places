<template>
  <div class="field">
    <h2>{{title}}</h2>
    <div class="block">
      <b-radio v-model="radio" native-value="Uit">
        Uit
      </b-radio>
      <b-radio v-model="radio" native-value="P2000">
        Politiemeldingen
      </b-radio>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      radio: "Uit"
    };
  },
  props: {
    categories: Array,
    title: String
  },
  watch: {
    radio: function() {
      this.$emit("selected", this.radio);
    }
  }
};
</script>

<style scoped>
.block {
  margin-left: 0.3em;
}
</style>
