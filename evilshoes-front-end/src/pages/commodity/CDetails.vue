<template>
  <div class="x-details">
    <el-row class="good">
      <!-- <el-col :span="2"></el-col> -->
      <el-col :span="24">
        <el-page-header @back="goBack" content="详情"></el-page-header>
        <img :src="'http://127.0.0.1:8000/media/' + commodity.image" alt="">
        <div class="det">
          <div class="dtitle">{{ commodity.name }}</div>
          <div class="dprice">
            <span>价格</span>
            <span>{{ '￥' + commodity.price }}</span>
          </div>
          <div class="count">
            <span>数量</span><el-input-number v-model="num" controls-position="right" @blur="handleBlur" :min="1" :max="10"></el-input-number>
          </div>
          <div class="dprice">
            <span>库存</span>
            <span style="color: rgb(90, 89, 89); font-size: 14px;">{{ commodity.storage }}</span>
          </div>
          <div class="btn">
            <el-button type="primary" @click="buy">立即购买</el-button>
            <el-button type="primary" icon="el-icon-shopping-cart-2" @click="addCart">加入购物车</el-button>
            <el-button type="primary" icon="el-icon-star-off" @click="collect(commodity.id)">收藏</el-button>
          </div>
        </div>
      </el-col>
      <!-- <el-col :span="2"></el-col> -->
    </el-row>
  </div>
</template>

<script>
export default {
  name: "x-details",
  data() {
    return {
      c_id: "",
      commodity: {},
      num: 1,
    };
  },
  mounted: function() {
    this.c_id = this.$route.params.cid;
    this.$axios({
      method: "get",
      url: "http://127.0.0.1:8000/commodity/detail/" + this.c_id
    }).then(response => {
      // window.console.log(response.data);
      if (response.data.code == 200) {
        this.commodity = response.data.data;
      } else {
        //
      }
    });
  },
  methods: {
    handleBlur(){
      if(this.num === undefined){
        this.num = 1
      }
    },
    goBack(){
      this.$router.go(-1)
    },
    buy(){
      var AUTH_TOKEN = window.localStorage.getItem('evil_token');
      this.$axios({
        method: "get",
        url: "http://127.0.0.1:8000/user/checklogin",
        headers: { Authorization: AUTH_TOKEN }
      }).then(response => {
        // window.console.log(response.data);
        if (response.data.code == 200) {
          this.$router.push({path: '/order/' + this.c_id + '_' + this.num});
        } else {
          this.$router.push({path: '/login'});
        }
      });
    },
    collect(cmd_id){
      // window.console.log(id)
      let AUTH_TOKEN = window.localStorage.getItem('evil_token')
      let c_id = cmd_id;
      let params = {commodity_id: c_id}
      this.$axios({
        method:"post",
        url:"http://127.0.0.1:8000/favourite/",
        headers:{Authorization: AUTH_TOKEN},
        data: params
      })
      .then(res=>{
        if(res.data.code == 200){
          this.$message({
            type: 'success',
            message:'添加收藏成功'
          })
        }else{
          // window.console.log('添加失败')
          this.message({
            type:'error',
            message:'添加收藏失败'
          })
        }
      })
    },
    addCart(){
      var AUTH_TOKEN = window.localStorage.getItem('evil_token');
      var params = {
        commodity_id: this.c_id,
        count: this.num,
      }
      this.$axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/cart/',
        data: params,
        headers: {Authorization: AUTH_TOKEN}
      }).then(response => {
        if(response.data.code == '200'){
          this.$message({
            type: 'success',
            message: '成功添加' + this.num + '件商品'
          });
        }else if(response.data.code == '30114'){
          // window.console.log('库存不足')
          this.$message({
            type: 'error',
            message: '库存不足，添加购物车失败'
          });
          
        }else{
          this.$router.push({path: '/login'});
        }
      });
    },
  }
};
</script>

<style>
.x-details{
  /* border: solid 1px red; */
}
.x-details .good{
  /* border: solid 1px red; */
}
.x-details .good .el-col:nth-child(1), .x-home .goods .el-col:nth-child(3){
  border: solid 1px white;
}
.x-details .good .el-col:nth-child(2){
  overflow: hidden;
}
.x-details .el-page-header{
  margin: 10px 0;
}
.x-details .good img{
  width: 350px;
  height: 350px;
  float: left;
  margin-right: 30px;
  border: solid 5px red;
  cursor: pointer;
}
.x-details .good .det{
  width: 600px;
  height: 350px;
  float: left;
  /* border: solid 1px red; */
  /* overflow: hidden; */
}
.x-details .good .det .dtitle{
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 30px;
  /* border: solid 1px red; */
}
.x-details .good .det .dprice{
  height: 40px;
  line-height: 40px;
}
.x-details .good .det .dprice span:nth-child(1){
  color: rgb(90, 89, 89);
  /* font-size: 16px; */
  margin-right: 25px;
}
.x-details .good .det .dprice span:nth-child(2){
  color: red;
  font-size: 20px;
}
.x-details .good .det .count{
  margin-bottom: 30px;
}
.x-details .good .det .count span{
  margin-right: 25px;
  color: rgb(90, 89, 89);
}
.x-details .good .det .btn{
  margin-top: 100px;
  padding-left: 100px;
  /* border: solid 1px red; */
}
.x-details .good .det .btn .el-button{
  margin-right: 15px;
}
</style>