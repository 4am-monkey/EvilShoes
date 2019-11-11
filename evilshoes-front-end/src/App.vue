<template>
  <div id="app">
    <x-header></x-header>
    <el-row class="bj">
      <el-col :span="2"></el-col>
      <el-col :span="20">
        <router-view :v-wechat-title='$route.meta.title'></router-view>
      </el-col>
      <el-col :span="2"></el-col>
    </el-row>
    <x-footer></x-footer>
  </div>
</template>

<script>
import Header from "./components/Header.vue"
import Footer from "./components/Footer.vue"

export default {
  name: "app",
  components: {
    'x-header': Header,
    'x-footer': Footer,
  },
  data(){
    return {

    }
  },
  methods: {
    
  },
};
</script>

<style>
body{
  margin: 0;
  padding: 0;
}
#app {
  width: 100%;
  /* font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50; */
  /* border: solid 1px rebeccapurple; */
}
#app .bj .el-col:nth-child(1), .x-home .goods .el-col:nth-child(3){
  border: solid 1px white;
}
</style>
