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
        <el-tab-pane label="我的订单">角色管理</el-tab-pane>
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
      addr_loading: false
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
    }
  }
};
</script>

<style>
.x-user {
  border: solid 1px red;
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
</style>