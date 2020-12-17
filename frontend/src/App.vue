<template>
  <v-app id="inspire">
    <v-navigation-drawer v-if="is_authenticated" v-model="drawer" app>
      <navigation-bar></navigation-bar>
    </v-navigation-drawer>

    <v-app-bar app elevate-on-scroll>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>

      <v-toolbar-title type="button" @click="$router.push({name: 'ListProducts'}).catch(err => {})">OkrestinoStore</v-toolbar-title>


      <v-spacer></v-spacer>

      {{user_info.last_name}} {{user_info.first_name}} {{user_info.middle_name}}
      <v-btn icon @click="$router.push({name: 'Profile'}).catch(err => {})">
        <v-icon>mdi-shopping-outline</v-icon>
      </v-btn>
      <v-menu offset-y left v-if="is_authenticated">
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on">
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>

        <v-list>
          <v-list-item>
            <v-list-item-title>
              <v-btn @click="$router.push({name: 'Profile'}).catch(err => {})" text>Мой профиль</v-btn>
            </v-list-item-title>
          </v-list-item>
          <v-list-item>
            <v-list-item-title>
              <v-btn @click="logout_in_system" text>Выход из аккаунта</v-btn>
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>

    </v-app-bar>

    <v-main>
      <v-container>
        <router-view></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import footerComponent from './components/barsComponents/Footer'
import NavigationBar from "./components/barsComponents/NavigationBar";
import {mapGetters, mapMutations} from "vuex";
import router from "@/router";

export default {
  name: 'App',
  data: () => ({ drawer: false }),

  components: {
    NavigationBar,
    footerComponent,
  },
  computed: {
    ...mapGetters(['is_authenticated', 'user_info'])
  },
  methods: {
    ...mapMutations(['clear_main_user_data']),
    logout_in_system() {
      this.clear_main_user_data()
      router.push({ name: 'Login' })
    },
  },
};
</script>
