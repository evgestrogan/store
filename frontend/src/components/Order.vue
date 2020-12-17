<template>
  <v-expansion-panels>
    <v-expansion-panel v-for="order in orders" :key="order.id"
    >
      <v-expansion-panel-header>
        <v-row no-gutters>
          <v-col cols="2">Заказ №{{order.id}}</v-col>
          <v-col cols="5" class="text--secondary">
              <span>Дата создания заказа: {{order.created}}</span>
          </v-col>
          <v-col cols="3" class="text--secondary">
              <span>Количество товаров: {{order.product.length}}</span>
          </v-col>
          <v-col cols="2">
            <v-chip v-if="order.status === 'О'" color="orange" label outlined>
              В обработке
            </v-chip>
            <v-chip v-if="order.status === 'П'" color="blue" label outlined>
              Подтвержден
            </v-chip>
            <v-chip v-if="order.status === 'З'" color="green" label outlined>
              Завершен
            </v-chip>
          </v-col>
        </v-row>
      </v-expansion-panel-header>
      <v-expansion-panel-content>
        <v-card>
          <v-card-title class="headline grey lighten-2">
            Информация о заказе
          </v-card-title>

          <v-card-text>

            <v-expansion-panels>
              <v-simple-table style="width: 100%">
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
                        Количество
                      </th>
                      <th class="text-left">
                        Цена за штуку
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="product in order.product" :key="product.id">
                      <td>{{ product.category.title }} {{ product.title }}</td>
                      <td>{{ Math.floor(product.weight * 100) / 100 }}кг.</td>
                      <td>{{ product.count }}шт.</td>
                      <td>{{ product.price }}р.</td>
                    </tr>
                  </tbody>
                </template>
              </v-simple-table>
            </v-expansion-panels>
          </v-card-text>
        </v-card>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script>
import {mapGetters} from "vuex";
const axios = require('axios').default;

export default {
  name: "Order",
  data: () => ({
    orders: [],
    sumWeight: 0,
    sumPrice: 0,
  }),
  computed: {
    ...mapGetters(['user_id'])
  },
  created() {
    axios({
      url: 'http://127.0.0.1:8000/api/order/',
      method: 'GET',
      params: {'user_id': this.user_id}
    })
    .then(resp => {
      this.orders = resp.data
    })
    .catch(err => {
    })
  }
}
</script>

<style scoped>

</style>