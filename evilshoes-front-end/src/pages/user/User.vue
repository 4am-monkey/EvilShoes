<template>
  <div class="x-user">
    <div class="uline">个人设置</div>
    <div>
      <el-tabs :tab-position="tabPosition">
        <el-tab-pane label="我的资料">
          <el-form label-width="80px" class="uinfo">
            <el-form-item label="账号">
              <span style="margin-right: 20px;">{{ username }}</span>
              <el-button round size="small">修改密码</el-button>
            </el-form-item>
          </el-form>
          <el-form
            :label-position="labelPosition"
            label-width="80px"
            :model="userInfo"
            class="uinfo"
          >
            <el-form-item label="昵称">
              <el-input v-model="userInfo.nickname"></el-input>
            </el-form-item>
            <el-form-item label="邮箱">
              <el-input v-model="userInfo.email"></el-input>
            </el-form-item>
            <el-form-item label="手机号">
              <el-input v-model="userInfo.telephone"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveInfo">保存</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="我的地址">
          <el-button class="ubtn" type="text" @click="dialogVisible = true">新增地址</el-button>
          <el-dialog title="新增地址" :visible.sync="dialogVisible" width="40%" @closed="handleClose">
            <el-form
              :label-position="labelPosition"
              label-width="100px"
              :model="address"
              class="uaddr"
            >
              <el-form-item label="收货地址">
                <el-input type="textarea" autosize placeholder v-model="address.addr"></el-input>
              </el-form-item>
              <el-form-item label="收件人姓名">
                <el-input v-model="address.name"></el-input>
              </el-form-item>
              <el-form-item label="收件人手机号">
                <el-input v-model="address.tel"></el-input>
              </el-form-item>
              <el-form-item label>
                <el-checkbox v-model="checked">设为默认地址</el-checkbox>
              </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
              <el-button @click="dialogVisible=false">取 消</el-button>
              <el-button type="primary" @click="saveAddr">确 定</el-button>
            </span>
          </el-dialog>
          <div class="ucount">已保存{{ addr_count }}条地址</div>
          <template>
            <el-table
              ref="multipleTable"
              :data="tableAddr"
              tooltip-effect="dark"
              style="width: 100%"
              border
              :row-class-name="tableRowClassName"
              v-loading="addr_loading"
            >
              <el-table-column label="收货人" width="150">
                <template slot-scope="scope">{{ scope.row.name }}</template>
              </el-table-column>
              <el-table-column label="收货地址" width="407">
                <template slot-scope="scope">{{ scope.row.addr }}</template>
              </el-table-column>
              <el-table-column label="收货人手机号" width="150">
                <template slot-scope="scope">{{ scope.row.tel }}</template>
              </el-table-column>
              <el-table-column label="操作" width="143">
                <template slot-scope="scope">
                  <el-button size="mini" @click="handleEdit(scope.$index, scope.row)">修改</el-button>
                  <el-button
                    size="mini"
                    type="danger"
                    @click="handleDelete(scope.$index, scope.row)"
                  >删除</el-button>
                </template>
              </el-table-column>
              <el-table-column label width="98">
                <template slot-scope="scope">
                  <el-button
                    size="mini"
                    @click="setDefault(scope.$index,scope.row)"
                  >{{ scope.row.default }}</el-button>
                </template>
              </el-table-column>
            </el-table>
          </template>
        </el-tab-pane>
        <el-tab-pane label="我的订单">
          <div class="myrow">
            <div>商品</div>
            <div>单价</div>
            <div>数量</div>
            <div>总价</div>
            <div>交易状态</div>
            <div>操作</div>
          </div>
          <div class="orders" v-for="order in orders" :key="order.id">
            <div class="time">
              <div class="crtime">{{ order.created_time }}</div>
              <div class="oid">订单号：{{ order.id }}</div>
              <div>删除</div>
            </div>
            <div class="hh">
              <div v-for="commodity in order.commodities" :key="commodity.id" class="commodities">
                <div class="comm">
                  <img :src="commodity.img" style="width: 30px; height: 30px;" alt />
                  <span class="title">{{ commodity.title }}</span>
                </div>
                <div class="price">{{ commodity.price }}</div>
                <div class="count">{{ commodity.count }}</div>
              </div>
            </div>
            <div class="kg">
              <div class="money">{{ order.money }}</div>
              <div class="status">{{ order.status }}</div>
            </div>
            <div style="clear: both; width: 100%; font-size: 12px;">收货地址：{{ order.addr }}</div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
export default {
  name: "x-user",
  data() {
    return {
      username: "",
      tabPosition: "left",
      labelPosition: "right",
      userInfo: {
        nickname: "",
        email: "",
        telephone: ""
      },
      address: {
        addr: "",
        name: "",
        tel: ""
      },
      dialogVisible: false,
      checked: false,
      tableAddr: [],
      is_default: false,
      addr_count: 0,
      addr_loading: false,
      orders: []
    };
  },
  mounted() {
    if (
      this.$route.path !=
      "/user/" + window.localStorage.getItem("evil_username")
    ) {
      this.$router.push({ path: "/" });
      this.$message.error("不可访问");
    }
    var AUTH_TOKEN = window.localStorage.getItem("evil_token");
    this.$axios({
      method: "get",
      url: "http://127.0.0.1:8000/user/info",
      headers: { Authorization: AUTH_TOKEN }
    }).then(response => {
      // window.console.log(response.data);
      if (response.data.code == 200) {
        var user = response.data.data;
        this.username = user.username;
        this.userInfo.nickname = user.nickname;
        this.userInfo.email = user.email;
        this.userInfo.telephone = user.telephone;
      } else {
        if (response.data.code == "10003") {
          this.$router.push({ path: "/" });
          this.$message.error("您在其他地方登录");
        } else {
          this.$router.push({ path: "/" });
          this.$message.error("请登录");
        }
      }
    });
    this.getAddr();
    this.getOrders();
  },
  methods: {
    saveInfo() {
      var AUTH_TOKEN = window.localStorage.getItem("evil_token");
      var params = {
        username: this.username,
        nickname: this.userInfo.nickname,
        email: this.userInfo.email,
        telephone: this.userInfo.telephone
      };
      this.$axios({
        method: "put",
        url: "http://127.0.0.1:8000/user/info",
        data: params,
        headers: { Authorization: AUTH_TOKEN }
      }).then(response => {
        // window.console.log(response.data);
        if (response.data.code == 200) {
          this.$message({
            message: "修改成功",
            type: "success"
          });
          window.localStorage.setItem("evil_nickname", this.userInfo.nickname);
          this.$router.go(0);
        } else {
          //
        }
      });
    },
    saveAddr() {
      this.dialogVisible = false;
      var AUTH_TOKEN = window.localStorage.getItem("evil_token");
      var params = {
        receiver: this.address.name,
        address: this.address.addr,
        receiver_phone: this.address.tel,
        is_default: this.checked
      };
      // window.console.log(params)
      this.$axios({
        method: "post",
        url: "http://127.0.0.1:8000/user/address",
        data: params,
        headers: { Authorization: AUTH_TOKEN }
      }).then(response => {
        // window.console.log(response.data);
        if (response.data.code == 200) {
          this.$message({
            message: "添加成功",
            type: "success"
          });
          this.getAddr();
        } else {
          //
        }
      });
    },
    handleClose() {
      this.address.addr = "";
      this.address.name = "";
      this.address.tel = "";
      this.checked = false;
    },
    handleEdit(index, row) {
      window.console.log(index);
      window.console.log(row);
      this.$message({
        type: "success",
        message: "功能开发中!"
      });
    },
    handleDelete(index, row) {
      window.console.log(index);
      var AUTH_TOKEN = window.localStorage.getItem("evil_token");
      var params = {
        addr_id: row.id
      };
      this.addr_loading = true;
      this.$axios({
        method: "delete",
        url: "http://127.0.0.1:8000/user/address",
        data: params,
        headers: { Authorization: AUTH_TOKEN }
      }).then(response => {
        if (response.data.code == "200") {
          this.$message({
            message: "删除成功",
            type: "success"
          });
          this.addr_loading = false;
          this.getAddr();
        }
      });
    },
    getAddr() {
      this.tableAddr = [];
      var AUTH_TOKEN = window.localStorage.getItem("evil_token");
      this.$axios({
        method: "get",
        url: "http://127.0.0.1:8000/user/address",
        headers: { Authorization: AUTH_TOKEN }
      }).then(response => {
        if (response.data.code == "200") {
          var addrs = response.data.data;
          this.addr_count = addrs.length;
          if (addrs.length == 0) {
            return;
          }
          var j = 0;
          if (addrs[0].is_default == 1) {
            var addr = {
              id: addrs[0].id,
              name: addrs[0].receiver,
              addr: addrs[0].address,
              tel: addrs[0].receiver_phone,
              default: "默认地址"
            };
            this.tableAddr.push(addr);
            j++;
            this.is_default = true;
          }
          for (var i = j; i < addrs.length; i++) {
            var addr2 = {
              id: addrs[i].id,
              name: addrs[i].receiver,
              addr: addrs[i].address,
              tel: addrs[i].receiver_phone,
              default: "设为默认"
            };
            this.tableAddr.push(addr2);
          }
          this.addr_loading = false;
        }
      });
    },
    setDefault(index, row) {
      var AUTH_TOKEN = window.localStorage.getItem("evil_token");
      if (row.default == "默认地址") {
        this.$message({
          type: "success",
          message: "已经是默认地址了哦!"
        });
      } else {
        this.$confirm("此操作将修改默认地址, 是否继续?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        })
          .then(() => {
            var params = {
              addr_id: row.id
            };
            this.addr_loading = true;
            this.$axios({
              method: "put",
              url: "http://127.0.0.1:8000/user/address",
              data: params,
              headers: { Authorization: AUTH_TOKEN }
            }).then(response => {
              if (response.data.code == "200") {
                this.$message({
                  type: "success",
                  message: "默认地址设置成功!"
                });
                this.getAddr();
              }
            });
          })
          .catch(() => {
            this.$message({
              type: "info",
              message: "已取消默认地址设置"
            });
          });
      }
    },
    tableRowClassName({ row, rowIndex }) {
      window.console.log("row: ", row);
      if (this.is_default) {
        if (rowIndex === 0) {
          return "warning-row";
        }
      }
    },
    formateDate(datetime) {
      function addDateZero(num) {
        return num < 10 ? "0" + num : num;
      }
      let d = new Date(datetime);
      let formatdatetime =
        d.getFullYear() +
        "-" +
        addDateZero(d.getMonth() + 1) +
        "-" +
        addDateZero(d.getDate()) +
        " " +
        addDateZero(d.getHours()) +
        ":" +
        addDateZero(d.getMinutes()) +
        ":" +
        addDateZero(d.getSeconds());
      return formatdatetime;
    },
    getOrders() {
      var STATUS = {
        0: "未付款",
        1: "等待发货",
        2: "配送中",
        3: "已完成",
        4: "支付失败",
        5: "已取消",
        6: "订单关闭"
      };
      var AUTH_TOKEN = window.localStorage.getItem("evil_token");
      this.$axios({
        method: "get",
        url: "http://127.0.0.1:8000/order/",
        headers: { Authorization: AUTH_TOKEN }
      }).then(response => {
        if (response.data.code == "200") {
          var orders = response.data.all_order;
          for (var i = 0; i < orders.length; i++) {
            var order = {};
            order.id = orders[i].id;
            order.created_time = this.formateDate(orders[i].create_time);
            order.status = STATUS[orders[i].status];
            order.money = orders[i].total_money;
            order.commodities = [];
            for (var j = 0; j < orders[i].commodities.length; j++) {
              var goods = {};
              goods.img = "";
              goods.title = orders[i].commodities[j].name;
              goods.price = orders[i].commodities[j].price;
              goods.count = orders[i].commodities[j].count;
              order.commodities.push(goods);
            }
            this.orders.push(order);
          }
        }
      });
    }
  }
};
</script>

<style>
.x-user {
  /* border: solid 1px red; */
}
.x-user .uline {
  font-size: 22px;
  font-weight: 700;
  padding-left: 20px;
  margin-bottom: 30px;
}
.x-user .uinfo {
  width: 350px;
}
.x-user .el-table .warning-row {
  background: oldlace;
  font-weight: 700;
}
.x-user .ubtn {
  margin-left: 30px;
  font-size: 18px;
}
.x-user .ucount {
  margin-left: 30px;
  margin-bottom: 10px;
  font-size: 12px;
}
.x-user .el-table {
  margin-left: 30px;
}
.x-user .myrow {
  /* border: solid 1px red; */
  margin-left: 30px;
  overflow: hidden;
  margin-bottom: 20px;
}
.x-user .myrow div {
  float: left;
  background: rgb(217, 229, 235);
}
.x-user .myrow div:nth-child(1) {
  width: 50%;
}
.x-user .myrow div:nth-child(2) {
  width: 10%;
}
.x-user .myrow div:nth-child(3) {
  width: 10%;
}
.x-user .myrow div:nth-child(4) {
  width: 10%;
}
.x-user .myrow div:nth-child(5) {
  width: 10%;
}
.x-user .myrow div:nth-child(6) {
  width: 35px;
}
.x-user .time {
  font-size: 14px;
  /* margin-bottom: -15px; */
  overflow: hidden;
  height: 30px;
  line-height: 30px;
  border-bottom: solid 1px rgb(245, 241, 241);
}
.x-user .time div:nth-child(1) {
  float: left;
  margin-right: 20px;
}
.x-user .time div:nth-child(2) {
  float: left;
}
.x-user .time div:nth-child(3) {
  float: right;
  cursor: pointer;
}
.x-user .time div:nth-child(3):hover {
  color: red;
}
.x-user .mytable {
  /* border: solid 1px red; */
}
.x-user .orders {
  /* border: solid 1px red; */
  width: 90%;
  overflow: hidden;
  margin-left: 30px;
  margin-bottom: 20px;
  /* background: snow; */
  border: solid 1px white;
  padding: 3px;
}
.x-user .orders:hover {
  border: solid 1px rgb(241, 86, 86);
  border-radius: 5px;
}
.x-user .hh {
  float: left;
  width: 76%;
  margin-top: 10px;
}
.x-user .orders .commodities {
  /* width: 90%; */
  /* border: solid 1px red; */
  overflow: hidden;
  margin-bottom: 10px;
}
.x-user .orders img {
  display: inline;
  cursor: pointer;
}
.x-user .orders span {
  /* border: solid 1px red; */
  margin-left: 20px;
  cursor: pointer;
}
.x-user .orders span:hover {
  color: red;
}
.x-user .orders .commodities .comm {
  float: left;
  width: 67%;
  margin-right: 4%;
  /* border: solid 1px yellow; */
}
.x-user .orders .commodities .price {
  float: left;
  width: 15%;
  /* border: solid 1px red; */
}
.x-user .orders .commodities .count {
  float: left;
  width: 14%;
  /* border: solid 1px red; */
}
.x-user .kg {
  overflow: hidden;
  width: 20%;
  margin-top: 10px;
  /* border: solid 1px red; */
}
.x-user .orders .money {
  /* border: solid 1px red; */
  float: left;
  width: 50%;
}
.x-user .orders .status {
  /* border: solid 1px red; */
  float: left;
  width: 50%;
  line-height: 16px;
}
</style>