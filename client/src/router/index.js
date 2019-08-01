import Vue from 'vue'
import Router from 'vue-router'
import Account from 'components/account'
import Tasks from 'components/Tasks.vue'
import Results from 'components/Results.vue'
import Login from 'components/login'
import store from '../store'

Vue.use(Router)

const ifNotAuthenticated = (to, from, next) => {
  if (!store.getters.isAuthenticated) {
    next()
    return
  }
  next('/Tasks')
}

const ifAuthenticated = (to, from, next) => {
  if (store.getters.isAuthenticated) {
    next()
    return
  }
  next('/login')
}

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Tasks',
      component: Tasks,
    },
    {
      path: '/Results',
      name: 'Results',
      component: Results,
    },
    {
      path: '/Tasks',
      name: 'Tasks',
      component: Tasks,
    },
    {
      path: '/account',
      name: 'Account',
      component: Account,
      beforeEnter: ifAuthenticated,
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
      beforeEnter: ifNotAuthenticated,
    },
  ],
})
