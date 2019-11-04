<template>
  <div id="app">
    <x-header></x-header>
    <router-view></router-view>
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
  }
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
</style>
