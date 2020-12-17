import Vue from 'vue'
import Vuex from 'vuex'
import user_store from './modules/user-store'
import content_store from './modules/content-store'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    user_store,
    content_store,
  },
})
