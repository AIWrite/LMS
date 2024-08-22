import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterView from '@/views/registerview.vue'
import createBook from '@/views/createBook.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/loginview.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView
  },
  {
    path: '/createSection',
    name: 'createSection',
    component: () => import('@/views/createSection.vue')
  },
  {
    path: '/updateSection/:id',
    name: 'updateSection',
    component: () => import('@/views/updateSection.vue')
  },
  {
    path: '/updateBook/:id',
    name: 'updateBook',
    component: () => import('@/views/updateBook.vue')
  },
  {
    path: '/updateUser',
    name: 'updateUser',
    component: () => import('@/views/updateUser.vue')
  },
  {
    path: '/request/:id',
    name: 'request',
    component: () => import('@/views/request.vue')
  },
  {
    path: '/grant/:id',
    name: 'grant',
    component: () => import('@/views/grant.vue')
  },
  {
    path: '/returns/:id',
    name: 'returns',
    component: () => import('@/views/returns.vue')
  },
  {
    path: '/views/:id',
    name: 'views',
    component: () => import('@/views/views.vue')
  },
  {
    path: '/revoke/:id',
    name: 'revoke',
    component: () => import('@/views/revoke.vue')
  },
  {
    path: '/createBook',
    name: 'createBook',
    component: createBook
  },
  {
    path: '/libdash',
    name: 'libDash',
    component: () => import('@/views/libDash.vue')
  },
  {
    path: '/userdash',
    name: 'userDash',
    component: () => import('@/views/userDash.vue')
  },
  {
    path: '/issueBook',
    name: 'issueBookDash',
    component: () => import('@/views/issueBook.vue')
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router