<template>
  <div class="x-home">
    <el-row class="types">
      <!-- <el-col :span="2"></el-col> -->
      <el-col :span="24">
        <ul>
          <li v-for="type in types" :key="type.id">{{ type.name }}</li>
        </ul>
      </el-col>
      <!-- <el-col :span="2"></el-col> -->
    </el-row>
    <el-row class="goods">
      <!-- <el-col :span="2"></el-col> -->
      <el-col :span="24">
          <el-card shadow="hover" 
                 :body-style="{ padding: '0px', border: '0px'}"
                 v-for="cmd in commodities" :key="cmd.id"
                 >
          <img :src="'http://127.0.0.1:8000/media/' + cmd.images" alt="" @click="toDetails(cmd.id)">
          <div @click="toDetails(cmd.id)">
            <div class="hprice">{{ '￥' + cmd.price }}</div>
            <div class="htitle">{{ cmd.name }}</div>
          </div>
        </el-card>
        <!-- </router-link> -->
      </el-col>
      <!-- <el-col :span="2"></el-col> -->
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
      types: [],
      commodities: [],
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
    this.$axios({
      method: "get",
      url: "http://127.0.0.1:8000/commodity"
    }).then(response => {
      // window.console.log(response.data);
      if (response.data.code == 200) {
        this.commodities = response.data.data;
      } else {
        //
      }
    });
  },
  methods: {
    toDetails(c_id){
      this.$router.push({path: '/details/' + c_id});
    }
  }
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
  padding-top: 10px;
  /* padding-left: 110px; */
  height: 60px;
  line-height: 60px;
  /* border-bottom: solid 1px red; */
}
.x-home ul li {
  display: inline;
  border: solid 2px black;
  border-radius: 0 70px 70px 0;
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
  overflow: hidden;
}
.x-home .goods .el-card{
  width: 250px;
  height: 330px;
  /* border: solid 1px #747171; */
  cursor: pointer;
  float: left;
  margin-right: 10px;
  margin-bottom: 30px;
}
.x-home .goods .el-card:hover{
  border: solid 1px rgb(245, 88, 88);
}
.x-home .goods .el-card img{
  width: 100%;
  height: 250px;
  display: block;
  /* border: solid 1px red;  */
}
.x-home .htitle{
  font-size: 14px;
  color: #404040;
  font-weight: 400;
  height: 50px;
  overflow: hidden;
}
.x-home .htitle:hover{
  color: rgb(245, 117, 117);
  text-decoration: underline;
}
.x-home .hprice{
  font-size: 16px;
  color: red;
  font-weight: 400;
}
</style>