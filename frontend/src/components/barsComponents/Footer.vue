<template>
  <v-footer padless app >
    <v-card class="text-center" width="100%">
      <v-divider></v-divider>
      <v-card-text>
        {{ new Date().getFullYear() }} — <strong>Store</strong>
      </v-card-text>
    </v-card>
  </v-footer>
</template>

<script>
export default {
  name: "Footer",

}
</script>

<style scoped>

</style>