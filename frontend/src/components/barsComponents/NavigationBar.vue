<template>
  <v-list nav dense>
    <v-list-item-group active-class="deep-purple--text text--accent-4">
      <v-list-item @click="$router.push({name: 'ListProducts'}).catch(err => {})">
        <v-list-item-title>Все продукты</v-list-item-title>
      </v-list-item>
      <v-list-item v-for="category in categories" :key="category.id" @click="$router.push({name: 'FilterListProducts', params: {'id_category': category.id}}).catch(err => {})">
        <v-list-item-title>{{category.title}}</v-list-item-title>
      </v-list-item>
    </v-list-item-group>
  </v-list>
</template>

<script>
import {mapGetters} from "vuex";
import router from "@/router";

export default {
  name: "NavigationBar",
  created() {
    this.$store.dispatch('get_categories')
    .catch(err => {
      router.push({ name: 'Login' })
    })
  },
  computed: {
    ...mapGetters(['categories'])
  },
}
</script>

<style scoped>

</style>