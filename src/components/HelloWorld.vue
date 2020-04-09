<template>
  <section class="section">
    <div>
  <label class="typo__label">Simple select / dropdown</label>
  <multiselect v-model="value" :options="categories" :multiple="true" :close-on-select="false" :clear-on-select="true" :hide-selected="true" :selectLabel="false" :preserve-search="true" placeholder="" label="category" track-by="category" :preselect-first="true">
    <template slot-scope="props"><span class="custom__tag"><span>{{ props.option.category }}</span><span class="custom__remove" @click="props.remove(props.option)">❌</span></span></template>
  </multiselect>
  <pre class="language-json"><code>{{ value  }}</code></pre>
</div>
    <h1 class="title">{{ msg }}</h1>
    <div class="content">
      <h2>Haai {{ coords }}</h2>
      <h3>Query:</h3>
      <ul>
        <li v-for="cat in categories" :key="cat.id">{{ cat }}</li>
        <!-- <li v-for="data in voorzieningFilterCat('Bioscoop')" :key="data.id">{{ data.name }}</li> -->
        <!-- <li> {{ dutchTitleCase('De Ijstuin') }} </li> -->
            <!-- <multiselect v-model="value" :options="options"></multiselect> -->
      </ul>
    </div>
</section>
</template>

<script>
import Multiselect from "vue-multiselect";
import locations from "../assets/functies.json";

export default {
  cat: "HelloWorld",
  components: { Multiselect },
  data() {
    return {
      coords: [],
      errors: [],
      value: null,
      locations
    };
  },
  props: {
    msg: String
  },
  methods: {
    voorzieningFilterCat: function(category) {
      return locations.filter(el => el.cat === category);
    }
  },
  computed: {
    categories: function() {
      // Get unique values, see https://medium.com/tomincode/removing-array-duplicates-in-es6-551721c7e53f
      const unique = (value, index, self) => {
        return self.indexOf(value) === index;
      };
      const values = locations.map(item => item.cat);
      const uniqueValuesArray = values.filter(unique).sort();
      const uniqueValues = uniqueValuesArray.map(item => ({ category: item }));
      const colors25 = [
        "#e1ad9b",
        "#90e1f3",
        "#ebd4ab",
        "#96b4df",
        "#cfe7b9",
        "#d4b4e5",
        "#b2c69a",
        "#e9b4cb",
        "#9fcaac",
        "#b7adcd",
        "#e3f1d2",
        "#b3d3f5",
        "#c7b69f",
        "#8cc4dc",
        "#f0dcd0",
        "#87c4b8",
        "#d8ccec",
        "#bdf0dd",
        "#dbc0c2",
        "#94d1d8",
        "#b4c4ad",
        "#c7dfee",
        "#a4beb8",
        "#cde8e2",
        "#afb9cb"
      ];
      uniqueValues.forEach((el, i) => (uniqueValues[i].color = colors25[i]));
      return uniqueValues;
    }
  },
  locations: locations
};
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css">
</style>

<style>
.custom__tag {
  display: inline-block;
  padding: 3px 12px;
  background: #96b4df;
  margin-right: 8px;
  margin-bottom: 8px;
  border-radius: 10px;
  cursor: pointer;
}
.custom__remove {
  font-size: 9px;
  padding-left: 5px;
}

.multiselect__tag {
  background: grey;
}

.multiselect__tag-icon:after {
  content: "\D7";
  color: white;
  font-size: 14px;
}

.multiselect__tag-icon:focus,
.multiselect__tag-icon:hover {
  background: dimgray;
}
.multiselect__option--highlight {
  background: dimgray;
  outline: none;
  color: #fff;
}
</style>
