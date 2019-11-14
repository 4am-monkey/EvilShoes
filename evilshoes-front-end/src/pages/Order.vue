<template>
  <div class="x-order">
    <div class="tou">
      <div class="px">拍下商品</div>
      <div class="bar">
        <el-steps :space="200" :active="0" finish-status="success">
          <el-step title="拍下商品"></el-step>
          <el-step title="待付款"></el-step>
          <el-step title="待收货"></el-step>
          <el-step title="交易成功"></el-step>
        </el-steps>
      </div>
    </div>
    <div class="ocon">确认收货地址</div>
    <div v-if="none" class="none">
      <span>还没有地址&nbsp;&nbsp;</span>
      <span>
        <el-link target="_blank" @click="addAddr">添加地址</el-link>
      </span>
    </div>
    <el-card shadow="hover" v-else v-for="addr in three_addrs" v-bind:key="addr.id">
      <el-radio v-model="radio" :label="addr.rlabel">寄往这个地址</el-radio>
      <div class="orec">{{ addr.name }}（收）</div>
      <div class="oline"></div>
      <div class="oaddr">{{ addr.addr }}</div>
    </el-card>
    <div class="yc" v-if="moreAddr">
      <el-collapse>
        <el-collapse-item title="更多地址">
          <el-card shadow="hover" v-for="addr in other_addrs" v-bind:key="addr.id">
            <el-radio v-model="radio" :label="addr.rlabel">寄往这个地址</el-radio>
            <div class="orec">{{ addr.name }}</div>
            <div class="oline"></div>
            <div class="oaddr">{{ addr.addr }}</div>
          </el-card>
        </el-collapse-item>
      </el-collapse>
    </div>
    <div style="height: 30px;"></div>
    <div class="ocon">确认订单信息</div>
    <el-table ref="multipleTable" :data="goodsInfo" tooltip-effect="dark" style="width: 93%" border>
      <el-table-column label="商品" width="558">
        <template slot-scope="scope">
          <img :src="scope.row.img" alt />
          <span>{{ scope.row.title }}</span>
        </template>
      </el-table-column>
      <el-table-column label="单价" width="150">
        <template slot-scope="scope">{{ scope.row.price }}</template>
      </el-table-column>
      <el-table-column label="数量" width="150">
        <template slot-scope="scope">{{ scope.row.count }}</template>
      </el-table-column>
      <el-table-column label="小计" width="150">
        <template slot-scope="scope">{{ scope.row.sum }}</template>
      </el-table-column>
    </el-table>
    <div class="hj">
      <div class="hj2">{{ total_price }}</div>
      <div class="hj1">合计</div>
    </div>
    <div class="tj">
      <el-button type="danger" plain @click="commitOrder">提交订单</el-button>
    </div>
  </div>
</template>

<script>
export default {
  name: "x-order",
  data() {
    return {
      c_id: this.$route.params.c_id,
      radio: "1",
      moreAddr: false,
      three_addrs: [],
      other_addrs: [],
      none: false,
      goodsInfo: [],
      total_price: 0
    };
  },
  methods: {
    getAddr() {
      var AUTH_TOKEN = window.localStorage.getItem("evil_token");
      this.$axios({
        method: "get",
        url: "http://127.0.0.1:8000/user/address",
        headers: { Authorization: AUTH_TOKEN }
      }).then(response => {
        if (response.data.code == "200") {
          var addrs = response.data.data;
          if (addrs.length == 0) {
            this.none = true;
            return;
          }
          var l = 0;
          var j = 3;
          if (addrs.length <= 3) {
            for (var i = 0; i < addrs.length; i++) {
              l++;
              var three_addr = {
                id: addrs[i].id,
                name: addrs[i].receiver,
                addr: addrs[i].address,
                rlabel: l.toString()
              };
              this.three_addrs.push(three_addr);
            }
          } else {
            this.moreAddr = true;
            for (var m = 0; m < j; m++) {
              l++;
              var three_addr2 = {
                id: addrs[m].id,
                name: addrs[m].receiver,
                addr: addrs[m].address,
                rlabel: l.toString()
              };
              this.three_addrs.push(three_addr2);
            }
            for (var n = j; n < addrs.length; n++) {
              l++;
              var other_addr = {
                id: addrs[n].id,
                name: addrs[n].receiver,
                addr: addrs[n].address,
                rlabel: l.toString()
              };
              this.other_addrs.push(other_addr);
            }
          }
        } else {
          this.$router.push("/login");
        }
      });
    },
    addAddr() {
      this.$router.push({
        path: "/user/" + window.localStorage.getItem("evil_username")
      });
    },
    getGoodsInfo() {
      var AUTH_TOKEN = window.localStorage.getItem("evil_token");
      var goodsInfo_str = this.$route.params.goods_info;
      var goodsInfo_arr = goodsInfo_str.split("&");
      var commodities_id = [];
      var commodities_count = [];
      for (var i = 0; i < goodsInfo_arr.length; i++) {
        var cid = goodsInfo_arr[i].split("_")[0];
        var count = goodsInfo_arr[i].split("_")[1];
        commodities_id.push(cid);
        commodities_count.push(count);
      }
      var params = {
        commodities_id: commodities_id
      };
      this.$axios({
        method: "post",
        url: "http://127.0.0.1:8000/commodity/buy",
        data: params,
        headers: { Authorization: AUTH_TOKEN }
      }).then(response => {
        if (response.data.code == "200") {
          var goods = response.data.commodities_info;
          for (var m = 0; m < goods.length; m++) {
            var commodity = {};
            commodity.id = goods[m].id;
            commodity.img = "http:127.0.0.1:8000/media/" + goods[m].images;
            commodity.title = goods[m].name;
            commodity.price = goods[m].price;
            commodity.count = commodities_count[m];
            commodity.sum = (commodity.price * commodity.count).toFixed(2);
            this.goodsInfo.push(commodity);
          }
          this.getTotalPrice();
        }
      });
    },
    getTotalPrice() {
      var total = 0;
      for (var i = 0; i < this.goodsInfo.length; i++) {
        total += parseFloat(this.goodsInfo[i].sum);
      }
      total = total.toFixed(2);
      this.total_price = total;
    },
    commitOrder() {
      if (this.moreAddr) {
        var addr_id = "";
        if (this.radio > 3) {
          addr_id = this.other_addrs[this.radio - 4].id;
        } else {
          addr_id = this.three_addrs[this.radio - 1].id;
        }
      } else {
        addr_id = this.three_addrs[this.radio - 1].id;
      }
      var sum = 0;
      var commodities = [];
      for (var i = 0; i < this.goodsInfo.length; i++) {
        var goods = {};
        goods.id = this.goodsInfo[i].id;
        goods.name = this.goodsInfo[i].title;
        goods.count = this.goodsInfo[i].count;
        goods.price = this.goodsInfo[i].price;
        commodities.push(goods);
        sum += parseInt(this.goodsInfo[i].count);
      }
      var params = {
        addr_id: addr_id,
        total_amount: sum,
        total_money: this.total_price,
        commodities: commodities
      };
      var AUTH_TOKEN = window.localStorage.getItem("evil_token");
      this.$axios({
        method: "POST",
        url: "http://127.0.0.1:8000/order/",
        data: params,
        headers: { Authorization: AUTH_TOKEN }
      }).then(response => {
        if (response.data.code == "200") {
          this.$message({
            type: "success",
            message: "添加订单成功"
          });
          var params2 = {
            order_id: response.data.data.order_id
          };
          this.$axios({
            method: "post",
            url: "http://127.0.0.1:8000/order/pay",
            data: params2,
            headers: { Authorization: AUTH_TOKEN }
          }).then(response => {
            if (response.data.code == "200") {
              var pay_url = response.data.pay_url;
              window.location.href = pay_url;
            }
          });
        } else if (response.data.code == "40103") {
          this.$message({
            type: "error",
            message: "库存不足！提交订单失败"
          });
        }
      });
    }
  },
  mounted() {
    this.getAddr();
    this.getGoodsInfo();
  }
};
</script>

<style>
.x-order .tou {
  overflow: hidden;
}
.x-order .px {
  font-size: 22px;
  font-weight: 700;
  width: 200px;
  border-bottom: solid 2px black;
  margin-bottom: 20px;
  float: left;
}
.x-order .bar {
  float: right;
  width: 500px;
  /* border: solid 1px red; */
}
.x-order .ocon {
  color: red;
  margin-bottom: 10px;
}
.x-order .el-card {
  width: 30%;
  float: left;
  margin-right: 15px;
  margin-bottom: 10px;
}
.x-order .el-card:hover {
  border: solid 1px rgb(245, 117, 117);
}
.x-order .el-card .orec {
  color: #67c23a;
  font-size: 14px;
  margin-bottom: 5px;
  margin-top: 5px;
}
.x-order .el-card .oaddr {
  color: #909399;
  margin-top: 5px;
}
.x-order .el-card .oline {
  border-bottom: solid 1px rgb(236, 234, 234);
}
.x-order .yc {
  clear: both;
  width: 95%;
}
.x-order .none span {
  font-size: 14px;
  line-height: 20px;
  display: inline;
  font-size: 14px;
}
.x-order .hj {
  overflow: hidden;
  height: 30px;
  padding: 5px;
  margin: 50px 80px 10px 0;
}
.x-order .hj .hj1 {
  float: right;
  line-height: 30px;
  margin-right: 10px;
}
.x-order .hj .hj2 {
  float: right;
  line-height: 30px;
  color: red;
}
.x-order .tj {
  float: right;
  margin-right: 80px;
}
.x-order .img {
  width: 30px;
  height: 30px;
  display: inline-block;
}
</style>