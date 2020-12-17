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
  name: "ListProducts",
  components: {
    productComponent,
  },
  computed: {
    ...mapGetters(['products'])
  },
  created: function () {
    this.$store.dispatch('get_user_info')
    .catch(err => { router.push({ name: 'Login' }) })

    this.$store.dispatch('get_products')
    .catch(err => { router.push({ name: 'Login' }) })
  },
}
</script>

<style scoped>

</style>