<template>
  <div class="x-header">
    <li v-for="type in types" :key="type.id">
    {{ type }}
  </li>
  </div>
</template>

<script>
// 在此处导入需要的组件
// 如：import Footer from "./components/Footer.vue"

export default {
  name: "x-header",
  data() {
    return {
      types: []
    };
  },
  methods: {

  }
};
</script>

<style>
</style>