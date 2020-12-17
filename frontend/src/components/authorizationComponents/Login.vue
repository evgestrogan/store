<template>
  <v-form ref="form" v-model="valid" lazy-validation align="center">
   <v-text-field v-model="login" :counter="25" :rules="nameRules" label="Логин" autocomplete="username" required></v-text-field>
    <v-text-field
      v-model="password"
      :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
      :rules="[passwordRules.required, passwordRules.min]"
      :type="show ? 'text' : 'password'"
      name="input-10-1"
      label="Пароль"
      hint="пароль должен быть длиннее 8 символов"
      counter
      autocomplete="current-password"
      @click:append="show = !show"
    ></v-text-field>

    <v-btn :disabled="!valid" color="success" class="mr-4" @click="login_in_system">
      Войти в систему
    </v-btn>
  </v-form>
</template>

<script>
import router from "@/router";

export default {
  name: "LoginForm",
  data: () => ({
    valid: false,
    login:'',
    show: false,
    password: '',
    nameRules: [
      v => !!v || 'Заполните поле',
      v => (v && v.length <= 25) || 'Слишком длинное',
    ],
    passwordRules: {
      required: value => !!value || 'Введите пароль',
      min: v => v.length >= 8 || 'Пароль должен быть не менее 8 символов',
    }
  }),

  methods: {
    login_in_system () {
      if (this.$refs.form.validate()) {
        this.$store.dispatch('authorization', { 'username': this.login, 'password': this.password })
        .then(resp => {
          router.push({name: 'ListProducts'})
        })
        .catch(err => {
          router.push({ name: 'Registration' })
        })
      }
    },
  },
}
</script>

<style scoped>

</style>