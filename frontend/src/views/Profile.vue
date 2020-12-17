<template>
  <v-row>
    <v-bottom-navigation :value="value" color="teal" grow>
      <v-btn @click="value='Корзина'">Корзина</v-btn>
      <v-btn @click="value='Заказы'">Заказы</v-btn>
    </v-bottom-navigation>
    <v-container v-if="value==='Корзина'" >
      <v-row>
        <v-col v-for="product in basket" :key="product.id" cols="6">
          <product-component :product="product" :page="'profile'" :order="product.id" @getOrders="get_orders"></product-component>
        </v-col>
      </v-row>
      <v-row class="justify-center">
        <v-dialog v-model="dialog" width="800">
          <template v-slot:activator="{ on, attrs }">
            <v-btn v-bind="attrs" v-on="on" outlined x-large @click="calculate">Оформить заказ</v-btn>
          </template>

          <v-card>
            <v-card-title class="headline grey lighten-2">
              Информация о заказе
            </v-card-title>

            <v-card-text>
              <v-simple-table>
                <template v-slot:default>
                  <thead>
                    <tr>
                      <th class="text-left">
                        Количество товаров
                      </th>
                      <th class="text-left">
                        Общий вес
                      </th>
                      <th class="text-left">
                        Сумма
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr :style="(sumWeight <= 1 && sumWeight > 0) ?  {'color': 'green'}: {'color': 'red'}">
                      <td>У вас: {{basket.length}} вида товаров</td>
                      <td>{{ Math.floor(sumWeight * 100) / 100 }}</td>
                      <td>{{ Math.floor(sumPrice * 100) / 100 }}</td>
                    </tr>
                  </tbody>
                </template>
              </v-simple-table>

              <v-expansion-panels>
                <v-expansion-panel>
                  <v-expansion-panel-header>
                    Подробности о заказе
                  </v-expansion-panel-header>
                  <v-expansion-panel-content>
                    <v-simple-table>
                      <template v-slot:default>
                        <thead>
                          <tr>
                            <th class="text-left">
                              Название товара
                            </th>
                            <th class="text-left">
                              Вес
                            </th>
                            <th class="text-left">
                              Общий вес
                            </th>
                            <th class="text-left">
                              Количество
                            </th>
                            <th class="text-left">
                              Цена за штуку
                            </th>
                            <th class="text-left">
                              Общая стоимость
                            </th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="product in basket" :key="product.id">
                            <td>{{ product.category.title }} {{ product.title }}</td>
                            <td>{{ Math.floor(product.weight * 100) / 100 }}кг.</td>
                            <td>{{ Math.floor(product.weight * product.count * 100) / 100 }}кг</td>
                            <td>{{ product.count }}шт.</td>
                            <td>{{ product.price }}р.</td>
                            <td>{{ Math.floor(product.price * product.count * 100) / 100 }}р.</td>
                          </tr>
                        </tbody>
                      </template>
                    </v-simple-table>

                  </v-expansion-panel-content>
                </v-expansion-panel>
              </v-expansion-panels>
            </v-card-text>

            <v-divider></v-divider>

            <v-card-actions>
              <v-btn x-large text color="red" v-if="sumWeight > 1">Вес вашего заказа превышает 1 кг</v-btn>
              <v-spacer></v-spacer>
              <v-btn v-if="sumWeight <= 1 && sumWeight > 0" x-large text @click="create_order">
                Оформить заказ
              </v-btn>
              <v-btn v-if="sumWeight > 1 || sumWeight <= 0" x-large text @click="dialog = false">
                Закрыть
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

      </v-row>
    </v-container>

    <order-component v-if="value==='Заказы'"></order-component>
  </v-row>
</template>

<script>
import {mapGetters} from "vuex";
import productComponent from "../components/Product";
import orderComponent from "../components/Order";

const axios = require('axios').default;

export default {
  name: "Profile",
  data: () => ({
    basket: [],
    value: 'Корзина',
    dialog: false,
    sumWeight: 0,
    sumPrice: 0,
    counts: [],
    products: [],
  }),
  components: {
    productComponent,
    orderComponent,
  },
  computed: {
    ...mapGetters(['user_id'])
  },
  methods: {
    create_list_products(order) {
      for (const product of this.basket) {
        this.products.push({'order_id': order, 'product_id': product.id, 'count': product.count})
      }
    },
    create_order() {
      axios({
        url: 'http://127.0.0.1:8000/api/order/',
        method: 'POST',
        data: {
          "user_id": this.user_id
        }
      })
      .then(resp => {
        this.create_list_products(resp.data.id)
        axios({
          url: 'http://127.0.0.1:8000/api/orders/',
          method: 'POST',
          data: {
            "products": this.products
          }
        })
        .then(resp => {
          this.dialog = false
          this.delete_order()
        })
      })
      .catch(err => {
      })
    },
    parse_orders(data) {
      for (const product of data.product) {
        for (const count of data.user_to_product) {
          if (this.user_id === count.user_id && product.id === count.product_id) {
            product.count = count.count
          }
        }
      }
      this.basket = data.product
    },
    get_orders() {
      axios({
        url: 'http://127.0.0.1:8000/api/users/' + this.user_id,
        method: 'GET',
      })
      .then(resp => {
        this.parse_orders(resp.data)
      })
      .catch(err => {
      })
    },
    calculate() {
      this.sumPrice = 0
      this.sumWeight = 0
      for (const product of this.basket) {
        this.sumPrice += parseFloat(product.price) * product.count
        this.sumWeight += parseFloat(product.weight) * product.count
      }
    },
    delete_order() {
      for (const product of this.basket) {
        this.$store.dispatch('delete_order', {
          'product_id': product.id,
          'user_id': this.user_id,
          'count': product.count
        })
        .then(resp => {
          this.get_orders()
        })
        .catch(err => {
          console.log(err)
        })
      }
    },
  },
  created() {
    this.get_orders()
  },
}
</script>

<style scoped>

</style>