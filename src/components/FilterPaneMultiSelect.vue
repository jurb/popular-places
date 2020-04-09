<template>
    <section>
        <p> {{  }} </p>
        <b-field label="Enter some tags">
            <b-taginput
                v-model="tags"
                :data="categories"
                autocomplete
                field="category"
                icon="label"
                placeholder="Add a tag"
                :open-on-focus="openOnFocus"
                @typing="getFilteredTags"
                @input="cleanSelectionList">
                <template slot-scope="props">
                    <strong>{{props.option.category}}</strong>
                </template>
                <template slot="empty">
                    There are no items
                </template>
            </b-taginput>
        </b-field>
        <pre style="max-height: 400px"><b>Tags:</b>{{ tags }}</pre>
    </section>
</template>

<script>
import locations from "../assets/functies.json";
const categoryData = getUniqueLocationCategories();
import differenceBy from "lodash/differenceBy";
export default {
  data() {
    return {
      categories: categoryData,
      isSelectOnly: false,
      openOnFocus: true,
      tags: []
    };
  },
  computed: {},
  methods: {
    getFilteredTags(text) {
      this.categories = categoryData.filter(option => {
        return (
          option.category
            .toString()
            .toLowerCase()
            .indexOf(text.toLowerCase()) >= 0
        );
      });
      const selectedCategoriesExcluded = differenceBy(
        this.categories,
        this.tags,
        "category"
      );
      this.categories = selectedCategoriesExcluded;
      console.log(this.categories);
    },
    cleanSelectionList(array) {
      console.log(array);
      const selectedCategoriesExcluded = differenceBy(
        this.categories,
        this.tags,
        "category"
      );
      this.categories = selectedCategoriesExcluded;
      console.log(this.categories);
    }
  }
};

// find a way to move this into the Vue object like a normal person
function getUniqueLocationCategories() {
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
</script>
