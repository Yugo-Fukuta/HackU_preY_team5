import { createRouter, createWebHistory } from 'vue-router'
import Search from '../views/Search.vue'
import Signup from '../views/Signup.vue'
import Signin from '../views/Signin.vue'
import Celebs from '../views/Celebs.vue'

const routes = [
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/',
    name: 'Search',
    component: Search
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup
  },
  {
    path: '/signin',
    name: 'Signin',
    component: Signin
  },
  {
    path: '/celebs/:celebName',
    name: 'Celebs',
    component: Celebs
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
