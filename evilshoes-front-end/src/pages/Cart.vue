<template>
  <div class="x-cart">
    <div class="ccontainer">
      <div class="ccheck">
        <el-checkbox
          :indeterminate="isIndeterminate"
          v-model="checkAll"
          @change="handleCheckAllChange"
        >全选</el-checkbox>
        <el-checkbox-group v-model="checkedGoods" @change="handleCheckedGoodsChange">
          <el-checkbox v-for="cmd in goods" :label="cmd" :key="cmd"></el-checkbox>
        </el-checkbox-group>
      </div>
      <div class="cright">
        <!-- <div>全选</div> -->
        <div class="cheader">
          <div>商品</div>
          <div>单价</div>
          <div>数量</div>
          <div>小计</div>
          <div>操作</div>
        </div>
        <div v-for="cart in carts" :key="cart.id" class="carts">
          <div>
            <img :src="cart.img" style="width: 60px; height: 60px;" alt="">
            <div>{{ cart.title }}</div>
          </div>
          <div>{{ cart.price }}</div>
          <div>
            <el-input-number size="mini" v-model="cart.count" :min="1" :max="10" 
                             @blur="handleBlur(cart.id)" @change="handleC"></el-input-number>
          </div>
          <div>{{ cart.sum }}</div>
          <div>删除</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const goodsOptions = [0, 1, 2, 3];
export default {
  name: "x-cart",
  data() {
    return {
      checkAll: false,
      checkedGoods: [],
      goods: goodsOptions,
      isIndeterminate: false,
      // ccount: [1, 2],
      carts: [
        {
          id: 0,
          c_id: 1001,
          img: "http://127.0.0.1:8000/media/commodity/20000_3424764_0__solar.jpg",
          title: "小白鞋",
          price: 100,
          count: 2,
          sum: 200
        },
        {
          id: 1,
          c_id: 1002,
          img: "http://127.0.0.1:8000/media/commodity/20000_3424764_0__solar.jpg",
          title: "小皮鞋小皮鞋小皮鞋小皮鞋小皮鞋小皮鞋小皮鞋小皮鞋小皮鞋小皮鞋小皮鞋",
          price: 50,
          count: 3,
          sum: 150
        }
      ],
      
      //
    };
  },

  methods: {
    handleCheckAllChange(val) {
      // window.console.log(val)
      this.checkedGoods = val ? goodsOptions : [];
      this.isIndeterminate = false;
      // window.console.log(this.checkedGoods)
    },
    handleCheckedGoodsChange(value) {
      let checkedCount = value.length;
      this.checkAll = checkedCount === this.goods.length;
      this.isIndeterminate =
        checkedCount > 0 && checkedCount < this.goods.length;
      // window.console.log(this.checkedGoods)
    },
    handleBlur(value){
      if(this.carts[value].count === undefined){
        this.carts[value].count = 1
      }
    },
  },
  created() {
    // let AUTH_TOKEN = window.localStorage.getItem("evil_token");
    // this.$axios({
    //   method: "get",
    //   url: "http://127.0.0.1:8000/cart",
    //   headers: { Authorization: AUTH_TOKEN }
    // }).then(res => {
    //   window.console.log(res);
    //   this.tableData = res.data.data;
    // });
  }
};
</script>

<style>
.x-cart {
}
.x-cart .ccontainer {
  overflow: hidden;
  /* border: solid 1px red; */
}
.x-cart .ccheck {
  float: left;
  width: 6%;
  margin-right: 2%;
  border: solid 1px red;
}
.x-cart .ccheck .el-checkbox {
  display: block;
  height: 30px;
  line-height: 30px;
  padding: 5px;
}
.x-cart .ccheck .el-checkbox-group .el-checkbox {
  display: block;
  height: 80px;
  margin-top: 20px;
  padding: 5px;
}
.x-cart .cheader {
  /* border: solid 1px red; */
  overflow: hidden;
  float: left;
  width: 88%;
  height: 30px;
  line-height: 30px;
  padding: 5px;
  background: rgb(243, 206, 206);
}
.x-cart .cright .cheader div:nth-child(1) {
  float: left;
  width: 52%;
}
.x-cart .cright .cheader div:nth-child(2) {
  float: left;
  width: 10%;
}
.x-cart .cright .cheader div:nth-child(3) {
  float: left;
  width: 24%;
}
.x-cart .cright .cheader div:nth-child(4) {
  float: left;
  width: 10%;
}
.x-cart .cright .cheader div:nth-child(5) {
  float: left;
  width: 4%;
}
.x-cart .carts {
  border: solid 1px white;
  overflow: hidden;
  float: left;
  width: 88%;
  height: 80px;
  margin-top: 20px;
  padding: 5px;
}
.x-cart .carts:hover{
  border: solid 1px rgb(241, 86, 86);
  border-radius: 5px;
}
.x-cart .cright .carts div:nth-child(1) {
  float: left;
  width: 52%;
}
.x-cart .cright .carts div:nth-child(1) img {
  display: block;
  float: left;
}
.x-cart .cright .carts div:nth-child(1) div {
  margin-left: 10px;
  /* float: left; */
  /* border: solid 1px red; */
  width: 80%;
}
.x-cart .cright .carts div:nth-child(2) {
  float: left;
  width: 10%;
}
.x-cart .cright .carts div:nth-child(3) {
  float: left;
  width: 24%;
}
.x-cart .cright .carts div:nth-child(4) {
  float: left;
  width: 10%;
}
.x-cart .cright .carts div:nth-child(5) {
  float: left;
  width: 4%;
}

</style>