import { createRouter, createWebHistory } from 'vue-router'
import Register from '../components/Register.vue'
import Login from '../components/Login.vue'
import GoodsList from '../components/GoodsList.vue'
import GoodsDetail from '../components/GoodsDetail.vue'
import CreateGoods from '../components/CreateGoods.vue'
import EditGoods from '../components/EditGoods.vue'
import OrderList from '../components/OrderList.vue'
import OrderDetail from '../components/OrderDetail.vue'
import UserCenter from '../components/UserCenter.vue'
import MyGoods from '../components/MyGoods.vue'
import WishList from '../components/WishList.vue'
import AdminDashboard from '../components/AdminDashboard.vue'
import AdminUsers from '../components/AdminUsers.vue'
import AdminGoods from '../components/AdminGoods.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: GoodsList
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/goods/:id',
    name: 'GoodsDetail',
    component: GoodsDetail
  },
  {
    path: '/goods/create',
    name: 'CreateGoods',
    component: CreateGoods
  },
  {
    path: '/goods/:id/edit',
    name: 'EditGoods',
    component: EditGoods
  },
  {
    path: '/orders',
    name: 'OrderList',
    component: OrderList
  },
  {
    path: '/orders/:id',
    name: 'OrderDetail',
    component: OrderDetail
  },
  {
    path: '/user',
    name: 'UserCenter',
    component: UserCenter
  },
  {
    path: '/user/center',
    redirect: '/user'
  },
  {
    path: '/user/goods',
    name: 'MyGoods',
    component: MyGoods
  },
  {
    path: '/user/wishes',
    name: 'WishList',
    component: WishList
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard
  },
  {
    path: '/admin/users',
    name: 'AdminUsers',
    component: AdminUsers
  },
  {
    path: '/admin/goods',
    name: 'AdminGoods',
    component: AdminGoods
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

