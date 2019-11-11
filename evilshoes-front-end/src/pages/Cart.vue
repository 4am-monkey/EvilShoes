<template>
  <div class="x-cart">
    <div class="px">购物车</div>
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
            <img :src="cart.img" style="width: 60px; height: 60px;" alt />
            <div>{{ cart.title }}</div>
          </div>
          <div>{{ cart.price }}</div>
          <div>
            <el-input-number
              size="mini"
              v-model="cart.count"
              :min="1"
              :max="10"
              @blur="handleBlur(cart.id)"
              @change="handleChange(cart.id)"
            ></el-input-number>
          </div>
          <div>{{ cart.sum }}</div>
          <div>删除</div>
        </div>
      </div>
      <div class="hj">
        <div class="hj2">{{ total_price }}</div>
        <div class="hj1">合计</div>
      </div>
      <div class="tj">
        <el-button type="danger" plain @click="countOrder">结算</el-button>
      </div>
    </div>
  </div>
</template>

<script>
const goodsOptions = [0, 1];
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
          img:
            "http://127.0.0.1:8000/media/commodity/20000_3424764_0__solar.jpg",
          title: "小白鞋",
          price: 100,
          count: 2,
          sum: 200
        },
        {
          id: 1,
          c_id: 1002,
          img:
            "http://127.0.0.1:8000/media/commodity/20000_3424764_0__solar.jpg",
          title:
            "小皮鞋小皮鞋小皮鞋小皮鞋小皮鞋小皮鞋小皮鞋小皮鞋小皮鞋小皮鞋小皮鞋",
          price: 50,
          count: 3,
          sum: 150
        }
      ],
      total_price: (0).toFixed(2),

      //
    };
  },

  methods: {
    handleCheckAllChange(val) {
      // window.console.log(val)
      this.checkedGoods = val ? goodsOptions : [];
      this.isIndeterminate = false;
      // window.console.log(this.checkedGoods)
      this.countSum();
    },
    handleCheckedGoodsChange(value) {
      let checkedCount = value.length;
      this.checkAll = checkedCount === this.goods.length;
      this.isIndeterminate =
        checkedCount > 0 && checkedCount < this.goods.length;
      // window.console.log(this.checkedGoods)
      this.countSum();
    },
    handleBlur(value) {
      if (this.carts[value].count === undefined) {
        this.carts[value].count = 1;
      }
      this.carts[value].sum = this.carts[value].price * this.carts[value].count;
      this.countSum();
    },
    handleChange(value) {
      this.carts[value].sum = this.carts[value].price * this.carts[value].count;
      this.countSum();
    },
    countOrder(){

    },
    countSum(){
      this.total_price = 0;
      this.total_price = parseFloat(this.total_price);
      for(var i = 0; i < this.checkedGoods.length; i++){
        this.total_price += this.carts[this.checkedGoods[i]].sum;
      }
      this.total_price = this.total_price.toFixed(2);
    }
  },
  mounted() {
    let AUTH_TOKEN = window.localStorage.getItem("evil_token");
    this.$axios({
      method: "get",
      url: "http://127.0.0.1:8000/cart/",
      headers: { Authorization: AUTH_TOKEN }
    }).then(response => {
      window.console.log(response);
      // this.tableData = res.data.data;
    });
    window.console.log(unescape('\u5b89\u8e0fNASA\u7537\u978b\u8dd1\u6b65\u978b2019\u65b0\u6b3eSEEED\u5168\u638c\u6c14\u57ab\u978b\u7537\u58eb\u8fd0\u52a8\u978b\u5b98\u7f51\u65d7\u8230'))
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
  /* border: solid 1px red; */
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
.x-cart .carts:hover {
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
.x-cart .hj {
  clear: both;
  overflow: hidden;
  height: 30px;
  padding: 5px;
  margin: 50px 40px 10px 0;
}
.x-cart .hj .hj1 {
  float: right;
  line-height: 30px;
  margin-right: 10px;
}
.x-cart .hj .hj2 {
  float: right;
  line-height: 30px;
  color: red;
}
.x-cart .tj {
  float: right;
  margin-right: 40px;
}
.x-cart .px {
  font-size: 22px;
  font-weight: 700;
  width: 200px;
  border-bottom: solid 2px black;
  margin-bottom: 20px;
}
</style>