<template>
  <v-row>
    <v-col v-for="product in products" :key="product.id" cols="4">
      <product-component :product="product" :page="'list'"></product-component>
    </v-col>
  </v-row>
</template>

<script>
import router from "@/router"
import {mapGetters} from "vuex";
import productComponent from "../components/Product"

export default {
  name: "FilterListProducts",
  components: {
    productComponent,
  },
  computed: {
    ...mapGetters(['products'])
  },
  methods: {
    getProducts: function () {
      this.$store.dispatch('get_products', this.$route.params.id_category)
      .catch(err => { router.push({ name: 'Login' }) })
    }
  },
  created: function () {
    this.getProducts()
  },
  watch: {
    $route(to, from) {
      this.getProducts()
    }
  },
}
</script>

<style scoped>

</style>