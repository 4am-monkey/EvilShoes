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
            <div @click="toDetails(cart.id)">{{ cart.title }}</div>
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
          <div @click="delCart(cart.c_id)">删除</div>
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
var goodsOptions = [];
export default {
  name: "x-cart",
  data() {
    return {
      checkAll: false,
      checkedGoods: [],
      goods: goodsOptions,
      isIndeterminate: false,
      carts: [],
      total_price: (0).toFixed(2),
      // maxkc: 0
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
      var AUTH_TOKEN = window.localStorage.getItem("evil_token");
      var params = {
        commodity_id: this.carts[value].c_id,
        count: this.carts[value].count
      };
      this.$axios({
        method: "put",
        url: "http://127.0.0.1:8000/cart/",
        data: params,
        headers: { Authorization: AUTH_TOKEN }
      }).then(response => {
        if (response.data.code == "200") {
          this.carts[value].sum =
            this.carts[value].price * this.carts[value].count;
          this.countSum();
        } else if (response.data.code == "30105") {
          //
          // window.console.log("库存不足！");
          this.$message({
            type: 'error',
            message: '库存不足'
          });
          this.carts[value].count -= 1;
        }
      });
    },
    countOrder() {
      if (this.checkedGoods.length == 0) {
        return;
      }
      var ids = "";
      for (var i = 0; i < this.checkedGoods.length; i++) {
        var index = this.checkedGoods[i];
        var c_id = this.carts[index].c_id.toString();
        var count = this.carts[index].count.toString();
        ids += c_id + "_" + count + "&";
      }
      ids = ids.slice(0, -1);
      this.$router.push({ path: "/order/" + ids });
    },
    countSum() {
      this.total_price = 0;
      for (var i = 0; i < this.checkedGoods.length; i++) {
        this.total_price += parseFloat(this.carts[this.checkedGoods[i]].sum);
      }
      this.total_price = this.total_price.toFixed(2);
    },
    toDetails(id) {
      this.$router.push({ path: "/details/" + this.carts[id].c_id });
    },
    delCart(id) {
      var AUTH_TOKEN = window.localStorage.getItem("evil_token");
      var params = {
        commodity_id: id
      };
      this.$axios({
        method: "delete",
        url: "http://127.0.0.1:8000/cart/",
        data: params,
        headers: { Authorization: AUTH_TOKEN }
      }).then(response => {
        if (response.data.code == "200") {
          goodsOptions = [];
          this.carts = [];
          this.getCarts();
          this.$message({
            type: "success",
            message: "删除成功"
          });
        }
      });
    },
    getCarts() {
      let AUTH_TOKEN = window.localStorage.getItem("evil_token");
      this.$axios({
        method: "get",
        url: "http://127.0.0.1:8000/cart/",
        headers: { Authorization: AUTH_TOKEN }
      }).then(response => {
        // window.console.log(response.data);
        var commodities = JSON.parse(response.data.commodities);
        // var commodities = response.data.commodities;
        var others = response.data.others;
        for (var i = 0; i < commodities.length; i++) {
          var cart = {};
          cart.id = i;
          cart.c_id = commodities[i].pk;
          cart.img =
            "http://127.0.0.1:8000/media/" + commodities[i].fields.images;
          cart.title = commodities[i].fields.name;
          cart.price = commodities[i].fields.price;
          cart.count = others[i].count;
          cart.sum = others[i].amount;
          this.carts.push(cart);
          goodsOptions.push(i);
        }
      });
    }
  },
  beforeCreate() {
    goodsOptions = [];
    this.carts = [];
  },
  mounted() {
    this.getCarts();
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
  color: white;
}
.x-cart .is-checked .el-checkbox__label {
  color: white !important;
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
  cursor: pointer;
}
.x-cart .cright .carts div:nth-child(1) div {
  margin-left: 10px;
  /* float: left; */
  /* border: solid 1px red; */
  width: 80%;
  cursor: pointer;
}
.x-cart .cright .carts div:nth-child(1) div:hover {
  color: red;
  text-decoration: underline;
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
.x-cart .cright .carts div:nth-child(5):hover {
  cursor: pointer;
  color: red;
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