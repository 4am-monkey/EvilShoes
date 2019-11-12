import Vue from 'vue'
import Router from 'vue-router'

import Home from "@/pages/Home.vue"

import Login from "@/pages/user/Login.vue"
import Register from "@/pages/user/Register.vue"
import User from "@/pages/user/User.vue"

// import CList from "@/pages/commodity/CList.vue"
import CDetails from "@/pages/commodity/CDetails.vue"

import Collection from "@/pages/Collection.vue"
import Cart from "@/pages/Cart.vue"
import Order from "@/pages/Order.vue"
import Search from "@/pages/Search.vue"

import Header2 from "@/components/Header2.vue"


Vue.use(Router)

export default new Router({
  routes: [
    // 首页
    {
      path: '/',
      component: Home,
      name: '首页',
      meta: {
        title: '邪 | 首页'
      }
    },
    // 用户
    {
      path: '/login',
      component: Login,
      name: '登录',
      meta: {
        title: '邪 | 登录'
      }
    },
    {
      path: '/register',
      component: Register,
      name: '注册',
      meta: {
        title: '邪 | 注册'
      }
    },
    {
      path: '/user/:nickname',
      component: User,
      name: '用户中心',
      meta: {
        title: '邪 | 用户中心'
      }
    },
    // 商品
    // {
    //   path: '/commodity',
    //   component: CList,
    //   name: '商品列表',
    //   meta: {
    //     title: '邪 | 登录'
    //   }
    // },
    {
      path: '/details/:cid',
      component: CDetails,
      name: '商品详情',
      meta: {
        title: '邪 | 商品详情'
      }
    },
    // 收藏
    {
      path: '/collection',
      component: Collection,
      name: '收藏夹',
      meta: {
        title: '邪 | 收藏夹'
      }
    },
    // 购物车
    {
      path: '/cart/:username',
      component: Cart,
      name: '购物车',
      meta: {
        title: '邪 | 购物车'
      }
    },
    // 订单
    {
      path: '/order/:goods_info',
      component: Order,
      name: '订单',
      meta: {
        title: '邪 | 订单'
      }
    },
    // 搜索
    {
      path: '/search/:key',
      component: Search,
      name: '搜索',
      meta: {
        title: '邪 | 搜索'
      }
    },
    // 测试
    {
      path: '/test',
      component: Header2,
      name: '测试'
    }
  ],
  mode: "history"
})
