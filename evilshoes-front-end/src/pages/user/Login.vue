<template>
  <div class="x-login">
    <div class="regname">
      <div class="regname-l">用户登录</div>
      <div class="regname-r">
        没有账号&nbsp;
        去<router-link to="/register"><el-link type="primary">注册</el-link></router-link>
      </div>
    </div>
    <el-form
      :label-position="loginLabelPosition"
      label-width="80px"
      :model="loginForm"
      ref="loginForm"
      status-icon>
      <el-form-item label="用户名" prop="username"
                    :rules="[{ required: true, message: '请输入用户名', trigger: 'blur' }]">
        <el-input v-model="loginForm.username" placeholder="用户名"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password"
                    :rules="[{ required: true, message: '请输入密码', trigger: 'blur' }]">
        <el-input type="password" v-model="loginForm.password" 
                  show-password
                  placeholder="密码">
        </el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="login('loginForm')">登录</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
  // 在此处导入需要的组件
  // 如：import Footer from "./components/Footer.vue"

  export default {
    name: 'x-login',
    data() {
      return {
        loginLabelPosition: "right",
        loginForm: {
          username: "",
          password: '',
        },
      }
    },
    methods: {
      login(formName) {
        // window.alert(LOGINED)
        this.$refs[formName].validate((valid) => {
          if (valid) {
            let param = {
              "username": this.loginForm.username,
              "password": this.loginForm.password,
            }
            this.$axios({
              method: 'post',
              url: 'http://127.0.0.1:8000/user/login',
              data: param
            }).then((response) => {
              // window.console.log(response.data);
              if(response.data.code == 200){
                // this.$message({
                //   message: '登录成功',
                //   type: 'success'
                // });
                window.localStorage.setItem('evil_token', response.data.data.token);
                window.localStorage.setItem('evil_nickname', response.data.nickname);
                window.localStorage.setItem('evil_username', response.data.username);
                this.$router.push({ path: '/'})
                this.$router.go(0);
                // this.$router.go(-1);
            }else{
              if(response.data.code == 10204){
                this.$message.error('用户名或密码错误！');
                this.loginForm.username = '';
                this.loginForm.password = '';
              }
            }
          });
        } else {
          window.console.log('error submit!!');
          return false;
        }
      });
    },
    }
}
</script>

<style>
.x-login {
  margin: 0 auto;
  width: 350px;
  /* border: solid 1px red; */
}
.x-login .regname{
  margin-top: 30px;
  margin-bottom: 15px;
  /* border: solid 1px yellow; */
}
.x-login .regname-l {
  display: inline;
  font-size: 22px;
  font-weight: 700;
  /* border: solid 1px green; */
}
.x-login .regname-r {
  float: right;
  height: 30px;
  line-height: 30px;
  display: inline;
  font-size: 14px;
  /* border: solid 1px green; */
}
.router-link-active {
    text-decoration: none;
    outline: none;
    color: white;
}
.x-login .regname-r a{
  outline: none;
}
</style>



