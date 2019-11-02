import Vue from 'vue'
import Router from 'vue-router'

import Home from "@/pages/Home.vue"

import Login from "@/pages/user/Login.vue"
import Register from "@/pages/user/Register.vue"
import User from "@/pages/user/User.vue"

import CList from "@/pages/commodity/CList.vue"
import CDetails from "@/pages/commodity/CDetails.vue"

import Cart from "@/pages/Cart.vue"
import Order from "@/pages/Order.vue"


Vue.use(Router)

export default new Router({
  routes: [
    // 首页
    {
      path: '/',
      component: Home,
      name: '首页'
    },
    // 用户
    {
      path: '/login',
      component: Login,
      name: '登录'
    },
    {
      path: '/register',
      component: Register,
      name: '注册'
    },
    {
      path: '/user/:userid',
      component: User,
      name: '用户中心'
    },
    // 商品
    {
      path: '/commodity',
      component: CList,
      name: '商品列表'
    },
    {
      path: '/commodity/:commodityid',
      component: CDetails,
      name: '用户中心'
    },
    // 购物车
    {
      path: '/cart/:userid',
      component: Cart,
      name: '购物车'
    },
    // 订单
    {
      path: '/order/:userid',
      component: Order,
      name: '订单列表'
    },
  ],
  mode: "history"
})
