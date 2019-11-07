<template>
  <div class="x-register">
    <div class="regname">
      <div class="regname-l">注册新用户</div>
      <div class="regname-r">已有账号&nbsp;
        去<router-link to="/login"><el-link type="primary">登录</el-link></router-link>
      </div>
    </div>
    <el-form
      :label-position="regLabelPosition"
      label-width="80px"
      :model="registerForm"
      ref="registerForm"
      status-icon :rules="rules"
    >
      <el-form-item
        prop="email"
        label="邮箱"
        :rules="[
          { required: true, message: '请输入邮箱地址', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }]">
        <el-input v-model="registerForm.email" placeholder="邮箱"></el-input>
      </el-form-item>
      <el-form-item label="手机号" prop="telephone"
                    :rules="[{ required: true, message: '请输入手机号', trigger: 'blur' }]">
        <el-input v-model="registerForm.telephone" placeholder="手机号"></el-input>
      </el-form-item>
      <el-form-item label="用户名" prop="username"
                    :rules="[{ required: true, message: '请输入用户名', trigger: 'blur' }]">
        <el-input v-model="registerForm.username" placeholder="设置后不可更改"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password_1">
        <el-input type="password" v-model="registerForm.password_1" 
                  autocomplete="off" show-password
                  placeholder="请设置登录密码">
        </el-input>
      </el-form-item>
      <el-form-item label="确认密码" prop="password_2">
        <el-input type="password" v-model="registerForm.password_2" 
                  autocomplete="off" show-password
                  placeholder="请确认登录密码">
        </el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="register('registerForm')">注册</el-button>
        <el-button @click="resetForm('registerForm')">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
// 在此处导入需要的组件
// 如：import Footer from "./components/Footer.vue"

export default {
  name: "x-register",
  data() {
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'));
        } else {
          if (this.registerForm.password_1 !== '') {
            this.$refs.registerForm.validateField('password_2');
          }
          callback();
        }
      };
      var validatePass2 = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'));
        } else if (value !== this.registerForm.password_1) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback();
        }
      };
    return {
      regLabelPosition: "right",
      registerForm: {
        email: "",
        telephone: "",
        username: "",
        password_1: '',
        password_2: '',
      },
      rules: {
          password_1: [
            { validator: validatePass, trigger: 'blur' },
            { required: true, message: '请输入密码', trigger: 'blur' }
          ],
          password_2: [
            { validator: validatePass2, trigger: 'blur' },
            { required: true, message: '请确认密码', trigger: 'blur' }
          ]
      }
    };
  },
  methods: {
    register(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          let param = {
            "email": this.registerForm.email,
            "telephone": this.registerForm.telephone,
            "username": this.registerForm.username,
            "password_1": this.registerForm.password_1,
            "password_2": this.registerForm.password_2,
          }
          this.$axios({
            method: 'post',
            url: 'http://127.0.0.1:8000/user/register',
            data: param
          }).then((response) => {
            if(response.data.code == 200){
              this.$message({
                  message: '注册成功',
                  type: 'success'
              });
              window.localStorage.setItem('evil_token', response.data.data.token);
              window.localStorage.setItem('evil_nickname', response.data.nickname);
              window.localStorage.setItem('evil_username', response.data.username);
              this.$router.push({ path: '/' });
              this.$router.go(0);
            }else{
              if(response.data.code == 10112){
                this.$message.error('用户名已被使用！');
                this.registerForm.username = '';
              }
            }
          });
        } else {
          window.console.log('error submit!!');
          return false;
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
  }
};
</script>

<style>
.x-register {
  margin: 0 auto;
  width: 350px;
  /* border: solid 1px red; */
}
.x-register .regname{
  margin-top: 30px;
  margin-bottom: 15px;
  /* border: solid 1px yellow; */
}
.x-register .regname-l {
  display: inline;
  font-size: 22px;
  font-weight: 700;
  /* border: solid 1px green; */
}
.x-register .regname-r {
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
.x-register .regname-r a{
  outline: none;
}
</style>