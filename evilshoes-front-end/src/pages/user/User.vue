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
          <el-button type="text" @click="dialogVisible = true">新增地址</el-button>
          <el-dialog
            title="新增地址"
            :visible.sync="dialogVisible"
            width="30%"
            :before-close="handleClose"
          >
            <el-form
              :label-position="labelPosition"
              label-width="100px"
              :model="address"
              class="uaddr"
            >
              <el-form-item label="收货地址">
                <el-input type="textarea" autosize placeholder="" v-model="userInfo.addr"></el-input>
              </el-form-item>
              <el-form-item label="收件人姓名">
                <el-input v-model="userInfo.name"></el-input>
              </el-form-item>
              <el-form-item label="收件人手机号">
                <el-input v-model="userInfo.tel"></el-input>
              </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
              <el-button @click="dialogVisible = false">取 消</el-button>
              <el-button type="primary" @click="saveAddr">确 定</el-button>
            </span>
          </el-dialog>
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
      dialogVisible: false
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
      window.console.log(response.data);
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
          // this.$router.go(0);
        } else {
          //
        }
      });
    },
    saveAddr() {
      this.dialogVisible = false;
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
  width: 300px;
}
</style>