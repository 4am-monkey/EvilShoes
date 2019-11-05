<template>
  <div class="x-home">
    <el-row class="types">
      <el-col :span="2"></el-col>
      <el-col :span="20">
        <ul>
          <li v-for="type in types" :key="type.id">{{ type.name }}</li>
        </ul>
      </el-col>
      <el-col :span="2"></el-col>
    </el-row>
    <el-row class="goods">
      <el-col :span="2"></el-col>
      <el-col :span="20">
        <el-card shadow="hover" :body-style="{ padding: '0px', border: '0px'}">
          <img src="http://127.0.0.1:8000/media/wolf.jpeg" alt="">
          <div>

          </div>
        </el-card>
      </el-col>
      <el-col :span="2"></el-col>
    </el-row>
  </div>
</template>

<script>
// 在此处导入需要的组件
// 如：import Footer from "./components/Footer.vue"

export default {
  name: "x-home",
  data() {
    return {
      types: []
    };
  },
  mounted: function() {
    this.$axios({
      method: "get",
      url: "http://127.0.0.1:8000/commodity/classify"
    }).then(response => {
      // window.console.log(response.data);
      if (response.data.code == 200) {
        this.types = response.data.data;
      } else {
        //
      }
    });
  },
  methods: {}
};
</script>

<style>
.x-home {
  /* border: solid 1px red; */
  padding: 0;
}
.x-home .types .el-col{
  /* border: solid 1px red; */
  height: 60px;
}
.x-home ul {
  list-style: none;
  padding: 0px;
  margin: 0px;
  /* padding-left: 110px; */
  height: 60px;
  line-height: 60px;
}
.x-home ul li {
  display: inline;
  border: solid 2px black;
  border-radius: 0 50px 50px 0;
  margin-right: 40px;
  padding: 5px;
  font-size: 20px;
  cursor: pointer;
  background: black;
  color: white;
}
.x-home ul li:hover {
  background: white;
  color: black;
}
.x-home .goods{
  margin-top: 40px;
}
.x-home .goods .el-col:nth-child(1), .x-home .goods .el-col:nth-child(3){
  border: solid 1px white;
}
.x-home .goods .el-col:nth-child(2){
  /* border: solid 1px red; */
}
.x-home .goods .el-card{
  width: 200px;
  height: 250px;
  border: solid 1px #747171;
}
.x-home .goods .el-card img{
  width: 100%;
  display: block;
  border: solid 1px red; 
}
</style>