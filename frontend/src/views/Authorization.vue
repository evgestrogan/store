<template>
  <div>
    <v-tabs class="authentication" fixed-tabs>
      <v-tab :to="{name: 'Login'}">
          Вход в систему
      </v-tab>
      <v-tab :to="{name: 'Registration'}">
        Регистрация
      </v-tab>
    </v-tabs>
    <router-view class="ma-auto" style="max-width: 700px"></router-view>
  </div>
</template>
