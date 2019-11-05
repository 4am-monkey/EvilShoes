<template>
  <div class="x-header">
    <el-row>
      <el-col :span="2">
        <div class="grid-content"></div>
      </el-col>
      <el-col :span="4">
        <div class="grid-content">
          <div class="logo"><router-link to="/">邪</router-link></div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="grid-content">
          <el-input v-model="ipt_search" placeholder="搜索邪网"></el-input>
          <el-button type="primary" icon="el-icon-search"></el-button>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="grid-content">
          <!-- 未登录 -->
          <template v-if="online">
            <div class="logined">
              <div class="cart">
                <router-link to="/cart">购物车</router-link>
              </div>
              <div>
                <router-link to="/user">{{ nickname }}</router-link>
              </div>
              <div>
                <router-link to="/collection">收藏</router-link>
              </div>
            </div>
          </template>
          <template v-else>
            <div class="non-login">
              <div>
                <router-link to="/login">登录</router-link>
              </div>
              <div>
                <router-link to="/register">注册</router-link>
              </div>
            </div>
          </template>
        </div>
      </el-col>
      <el-col :span="2">
        <div class="grid-content"></div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
// 在此处导入需要的组件
// 如：import Footer from "./components/Footer.vue"
// const username = window.localStorage.getItem('evil_username')
export default {
  name: "x-header",
  props: ["logined"],
  data() {
    return {
      online: this.global.online,
      nickname: 'default',
      ipt_search: "",
    };
  },
  mounted: function() {
    var AUTH_TOKEN = window.localStorage.getItem('evil_token');
    if(AUTH_TOKEN == null){
      this.global.setOnline(false);
      this.online = this.global.online;
    }else{
      this.$axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/user/checklogin',
        headers: {'Authorization': AUTH_TOKEN}
      }).then((response) => {
          // window.console.log(response.data);
          if(response.data.code == 200){
            this.global.setOnline(true);
            this.online = this.global.online;
            this.nickname = window.localStorage.getItem('evil_nickname');
          }else{
            this.global.setOnline(false);
            this.online = this.global.online;
          }
        });
    }
  },
  methods: {

  }
};
</script>

<style>
.x-header .el-row {
  margin-bottom: 10px;
  /* border: solid 1px red; */
  background: black;
  color: white;
  padding: 10px 0;
}
.x-header .el-col {
  /* border: solid 1px yellow; */
}
.x-header .el-col:nth-child(4) {
  text-align: right;
}
.x-header .grid-content {
  height: 40px;
  line-height: 40px;
}
.x-header .logo {
  width: 90px;
  height: 40px;
  /* border: solid 1px white; */
  color: white;
  font-size: 36px;
}
.x-header .el-input {
  width: 300px;
  height: 35px;
  line-height: 35px;
  border-radius: 5px 0 0 5px;
  /* border: solid 1px yellow; */
}
.x-header .el-input__inner {
  /* border: solid 1px red; */
  height: 35px;
  line-height: 35px;
  border: solid 1px white;
  border-radius: 5px 0 0 5px;
  background: white;
}
.x-header .el-input__inner:focus,
.x-header .el-input__inner:hover {
  background: white;
  border: solid 1px white;
}
.x-header .el-button {
  padding: 9px 20px 10px 20px;
  border-radius: 0 5px 5px 0;
}
.x-header .el-button .el-icon-search {
  font-weight: 700;
}
.x-header .el-button--primary,
.x-header .el-button--primary:focus {
  background: rgba(201, 199, 199, 0.5);
  border: solid 1px white;
  border-left: 0;
}
.x-header .el-button--primary:hover {
  border: solid 1px white;
  border-left: 0;
  background: rgb(24, 22, 22);
}
.x-header .non-login, .x-header .logined {
  /* border: solid 1px rgb(230, 8, 238); */
  overflow: hidden;
}
.x-header .non-login > div, .x-header .logined > div {
  float: right;
  width: 60px;
  margin-right: 30px;
  cursor: pointer;
  text-align: center;
  font-size: 22px;
  font-weight: 700px;
}
.x-header .logined .cart{
  width: 80px;
}
.x-header .non-login div:hover, .x-header .logined div:hover {
  background: #0b0b0b;
  border-bottom: solid 2px white;
}
.x-header .non-login div a, .x-header .logined div a {
  text-decoration: none;
  outline: none;
  color: white;
}
.router-link-active {
  text-decoration: none;
  outline: none;
  color: white;
}
</style>





