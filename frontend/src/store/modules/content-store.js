const axios = require('axios').default;

export default {
    state: {
        categories: [],
        products: [],
    },
    mutations: {
        state_categories_data(state, response) {
            state.categories = response.data
        },
        clear_categories_data(state) {
            state.categories = []
        },
        state_products_data(state, response) {
            state.products = response.data
        },
        clear_products_data(state) {
            state.products = []
        },
    },
    actions: {
        async get_categories({ commit }) {
            return await new Promise((resolve, reject) => {
	            axios({url: 'http://127.0.0.1:8000/api/categories/',
                    method: 'GET',
                })
	            .then(resp => {
	                commit('state_categories_data', resp)
                    resolve(resp)
	            })
	            .catch(err => {
	                commit('state_categories_data')
	                reject(err)
	            })
	        })
        },
        async get_products({ commit }, id='') {
            commit('clear_products_data')
            return await new Promise((resolve, reject) => {
	            axios({url: 'http://127.0.0.1:8000/api/products/' + id,
                    method: 'GET',
                })
	            .then(resp => {
	                commit('state_products_data', resp)
                    resolve(resp)
	            })
	            .catch(err => {
	                commit('clear_products_data')
	                reject(err)
	            })
	        })
        },
        async create_order({ commit }, data) {
            return await new Promise((resolve, reject) => {
	            axios({
                    url: 'http://127.0.0.1:8000/api/users/',
                    method: 'POST',
                    data: {
	                    'product_id': data.id_product,
                        'user_id': data.id_user,
                        'count': data.count,
                    }
                })
	            .then(resp => {
                    resolve(resp)
	            })
	            .catch(err => {
	                reject(err)
	            })
	        })
        },
        async delete_order({ commit }, data) {
            return await new Promise((resolve, reject) => {
	            axios({
                    url: 'http://127.0.0.1:8000/api/users/',
                    data: data,
                    method: 'DELETE',
                })
	            .then(resp => {
                    resolve(resp)
	            })
	            .catch(err => {
	                reject(err)
	            })
	        })
        },
    },
    getters: {
        categories: state => state.categories,
        products: state => state.products,
    }
}