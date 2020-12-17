const axios = require('axios').default;
import VueJwtDecode from 'vue-jwt-decode'

export default {
    state: {
        user_id: null,
        is_authenticated: false,
        user_info: {
            "id": null,
            "email": "",
            "number_phone": "",
            "last_name": "",
            "first_name": "",
            "middle_name": "",
            "username": "",
        }
    },
    mutations: {
        state_main_user_data(state, response) {
            const refresh_token = response.data.refresh
            const access_token = response.data.access
            localStorage.setItem('refresh_token', refresh_token)
            axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token
            const user = VueJwtDecode.decode(access_token)
            state.user_id = user.user_id
            state.is_authenticated = true
        },
        clear_main_user_data(state) {
            localStorage.removeItem('refresh_token')
            delete axios.defaults.headers.common['Authorization']
            state.user_id = null
            state.is_authenticated = false
        },
        state_user_info(state, response) {
            state.user_info = response.data
        },
    },
    actions: {
        async authorization({ commit }, user) {
            return await new Promise((resolve, reject) => {
	            axios({url: 'http://127.0.0.1:8000/authentication/access/',
                    data: user,
                    method: 'POST',
                })
	            .then(resp => {
	                commit('state_main_user_data', resp)
                    resolve(resp)
	            })
	            .catch(err => {
	                commit('clear_main_user_data')
	                reject(err)
	            })
	        })
        },
        async registration({ commit }, user) {
            return await new Promise((resolve, reject) => {
	            axios({url: 'http://127.0.0.1:8000/authentication/users/',
                    data: user,
                    method: 'POST',
                })
	            .then(resp => {
                    resolve(resp)
	            })
	            .catch(err => {
	                reject(err)
	            })
	        })
        },
        async refresh({ commit }) {
            return await new Promise((resolve, reject) => {
                axios({
                    url: 'http://127.0.0.1:8000/authentication/refresh/',
                    data: { refresh: localStorage.getItem('refresh_token') },
                    method: 'POST',
                })
                .then(resp => {
                    commit('state_main_user_data', resp)
                    resolve(resp)
                })
                .catch(err => {
                    commit('clear_main_user_data')
                    reject(err)
                })
            })
        },
        async get_user_info({ commit }) {
            return await new Promise((resolve, reject) => {
                axios.get( 'http://127.0.0.1:8000/authentication/users/me/')
                .then(resp => {
                    commit('state_user_info', resp)
                    resolve(resp)
                })
                .catch(err => {
                    reject(err)
                })
            })
        },
    },
    getters: {
        is_authenticated: state => state.is_authenticated,
        user_id: state => state.user_id,
        user_info: state => state.user_info,
    }
}