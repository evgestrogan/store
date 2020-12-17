import Vue from 'vue'
import store from '../store/index'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'ListProducts',
    component: () => import('../views/ListProducts.vue'),
    meta: {
      authentication: true,
    },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue'),
    meta: {
      authentication: true,
    },
  },
  {
    path: '/:id_category',
    name: 'FilterListProducts',
    component: () => import('../views/FilterListProducts.vue'),
    meta: {
      authentication: true,
    },
  },
  // {
  //   path: '/:id',
  //   name: 'Category',
  //   component: () => import('../views/Home.vue'),
  //   meta: {
  //     authentication: true,
  //   },
  // },
  {
    path: '/authorization',
    name: 'Authorization',
    component: () => import('../views/Authorization.vue'),
    meta: {
      authentication: false,
    },
    children: [
      {
        path: 'login',
        name: 'Login',
        component: () => import('../components/authorizationComponents/Login'),
        meta: {
          authentication: false,
        },
      },
      {
        path: 'registration',
        name: 'Registration',
        component: () => import('../components/authorizationComponents/Registration'),
        meta: {
          authentication: false,
        },
      }
    ]
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  if (!to.matched.some(record => record.meta.authentication)) {
    store.dispatch('refresh')
    .then(() => next({ name: 'ListProducts' }))
    .catch(() => next())
  } else {
    store.dispatch('refresh')
    .then(() => next())
    .catch(() => next({ name: 'Login' }))
  }
})

export default router
