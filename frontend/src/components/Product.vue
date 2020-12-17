<template>
  <v-card class="mx-auto my-12" height="500">
    <v-snackbar v-model="snackbar" :timeout="2000" color="success" absolute>
      {{product.title}} {{message}}
    </v-snackbar>
    <v-carousel height="200">
      <v-carousel-item v-for="(photo, i) in product.photo" :key="i">
        <v-img :src="'http://127.0.0.1:8000/media/' + photo.photo" height="100%">
        </v-img>
      </v-carousel-item>
    </v-carousel>
    <v-card-title>{{product.title}}</v-card-title>
    <v-card-text>
      <div>{{product.description}}</div>
    </v-card-text>

    <v-divider class="mx-4"></v-divider>

    <v-card-title>Дополнительная информация</v-card-title>
    <v-card-text>
      <v-chip-group v-if="page === 'list'">
        <v-chip >вес: {{ Math.floor(product.weight * 100) / 100 }} кг.</v-chip>
        <v-chip >цена: {{product.price}}р.</v-chip>
        <v-chip v-if="product.presence" color="green">В наличии</v-chip>
        <v-chip v-else color="red">Отсутствует</v-chip>
      </v-chip-group>
      <v-chip-group v-else>
        <v-chip color="green">У вас в корзине {{product.count}} штук</v-chip>
        <v-chip >Общий вес: {{Math.floor(product.weight * product.count * 100) / 100}} кг</v-chip>
        <v-chip >Цена: {{Math.floor(product.price * product.count * 100) / 100}}р.</v-chip>
      </v-chip-group>
    </v-card-text>
    <v-card-actions v-if="!snackbar">
      <v-dialog v-model="dialog_add" width="500">
        <template v-slot:activator="{ on, attrs }">
          <v-btn v-if="page === 'list'" color="deep-purple lighten-2" text v-bind="attrs" v-on="on" :disabled="!product.presence">
            Добавить в корзину
          </v-btn>
        </template>
        <v-card>
          <v-card-title class="headline grey lighten-2">
            Выберите количество товара
          </v-card-title>
          <v-card-text>
            <v-form ref="form" v-model="valid" lazy-validation align="center">
              <v-text-field type="number" v-model="count" :rules="countRules" label="Требуемое количество:" required></v-text-field>
              <v-btn color="primary" text @click="create_order" :disabled="!valid">
                Добавить в корзину
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-dialog>


      <v-dialog v-model="dialog_delete" width="500">
        <template v-slot:activator="{ on, attrs }">
          <v-btn v-if="page === 'profile'" color="deep-purple lighten-2" text v-bind="attrs" v-on="on" :disabled="!product.presence">
            Удалить из корзины
          </v-btn>
        </template>
        <v-card>
          <v-card-title class="headline grey lighten-2">
            Выберите количество товара
          </v-card-title>
          <v-card-text>
            <v-form ref="form" v-model="valid" lazy-validation align="center">
              <v-text-field type="number" v-model="count" :rules="countRules" label="Требуемое количество:" required></v-text-field>
              <v-btn color="primary" text @click="delete_order" :disabled="!valid">
                Удалить из корзины
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-dialog>

    </v-card-actions>
  </v-card>
</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "Product",
  props: {
    product: Object,
    page: String,
  },
  data: () => ({
    snackbar: false,
    message: '',
    count: 1,
    dialog_add: false,
    dialog_delete: false,
    valid: false,
    countRules: [
      v => !!v || 'Заполните поле',
      v => (v && v >= 0) || 'Введите корректное значение',
    ],
  }),
  components: {

  },
  computed: {
    ...mapGetters(['user_id'])
  },
  methods: {
    create_order() {
      this.dialog_add = false
      this.$store.dispatch('create_order', { 'id_product': this.product.id, 'id_user': this.user_id, 'count': this.count })
      .then(resp => {
        this.snackbar = true
        this.message = 'добавлено в корзину'
      })
      .catch(err => {
        console.log(err)
      })
    },
    delete_order() {
      this.dialog_delete = false
      this.$store.dispatch('delete_order', {'product_id': this.product.id, 'user_id': this.user_id, 'count': this.count})
      .then(resp => {
        this.$emit('getOrders')
      })
      .catch(err => {
        console.log(err)
      })
    },
  },
}
</script>

<style scoped>

</style>