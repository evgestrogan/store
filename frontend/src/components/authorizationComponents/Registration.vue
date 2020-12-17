<template>
  <v-form ref="form" v-model="valid" lazy-validation align="center">
    <v-text-field v-model="login" :counter="150" :rules="[rules.required, rules.min150]" label="Логин" autocomplete="username" required></v-text-field>
    <v-text-field
      v-model="password"
      :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
      :rules="[rules.required, rules.min9]"
      :type="show ? 'text' : 'password'"
      name="input-10-1"
      label="Пароль"
      hint="пололь должен быть длиннее 8 символов"
      counter
      autocomplete="new-password"
      @click:append="show = !show"
    ></v-text-field>

    <v-text-field
      v-model="rePassword"
      :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
      :rules="[rules.required, rules.min9, passwordConfirmationRule]"
      :type="show ? 'text' : 'password'"
      name="input-10-1"
      label="Повторите пароль"
      hint="пололь должен быть длиннее 8 символов"
      autocomplete="current-password"
      counter
      @click:append="show = !show"
    ></v-text-field>

    <v-text-field v-model="email" :rules="emailRules" label="E-mail" autocomplete="email" required></v-text-field>

    <v-divider></v-divider>

    <v-text-field v-model="lastname" :counter="150" :rules="[rules.required, rules.min150]" label="Фамилия" required></v-text-field>
    <v-text-field v-model="firstname" :counter="150" :rules="[rules.required, rules.min150]" label="Имя" required></v-text-field>
    <v-text-field v-model="middle_name" :counter="150" :rules="[rules.required, rules.min150]" label="Отчество" required></v-text-field>
    <v-text-field v-model="phone_number" :counter="9" :rules="[rules.required, rules.len9]" label="Номер телефона" required prefix="+375"></v-text-field>

    <v-btn :disabled="!valid" color="success" class="mr-4" @click="validate">
      Зарегестрироваться
    </v-btn>

  </v-form>
</template>

<script>
import router from "@/router";

export default {
  name: "RegisterForm",
  data: () => ({
    valid: false,
    lastname: '',
    firstname: '',
    middle_name: '',
    phone_number: '',
    login:'',
    show: false,
    password: '',
    rePassword: '',
    email: '',
    rules: {
      required: v => !!v || 'Заполните поле',
      min150: v => (v && v.length <= 150) || 'Слишком длинное',
      min9: v => v.length >= 8 || 'Пароль должен быть не менее 8 символов',
      len9: v => (v && v.length === 9 ) || 'Введите 9 цифр',
    },
    emailRules: [
      v => !!v || 'Введите свою почту',
      v => /.+@.+\..+/.test(v) || 'Вы неправльньно заполниле поле',
    ],
  }),
  computed: {
    passwordConfirmationRule() {
      return () => (this.password === this.rePassword) || 'Пароли не совпадают'
    }
  },

  methods: {
    validate () {
      if (this.$refs.form.validate()) {
        this.$store.dispatch('registration',
          {
            'username': this.login,
            'password': this.password,
            'email': this.email,
            'first_name': this.firstname,
            'last_name': this.lastname,
            'middle_name': this.middle_name,
            'number_phone': this.phone_number,
          })
        .then(resp => {
          this.$store.dispatch('authorization', { 'username': this.login, 'password': this.password })
          .then(resp => {
            router.push({ name: 'Home' })
          })
        })
      }
    },
  },
}
</script>

<style scoped>

</style>