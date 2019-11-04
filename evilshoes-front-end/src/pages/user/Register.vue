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
      class="demo-dynamic"
      status-icon :rules="rules"
    >
      <el-form-item
        prop="email"
        label="邮箱"
        :rules="[
          { required: false, message: '请输入邮箱地址', trigger: 'blur' },
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
      <el-form-item label="密码" prop="pass">
        <el-input type="password" v-model="registerForm.pass" 
                  autocomplete="off" show-password
                  placeholder="请设置登录密码">
        </el-input>
      </el-form-item>
      <el-form-item label="确认密码" prop="checkPass">
        <el-input type="password" v-model="registerForm.checkPass" 
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
  name: "x-header",
  data() {
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'));
        } else {
          if (this.registerForm.checkPass !== '') {
            this.$refs.registerForm.validateField('checkPass');
          }
          callback();
        }
      };
      var validatePass2 = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'));
        } else if (value !== this.registerForm.pass) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback();
        }
      };
    return {
      regLabelPosition: "left",
      registerForm: {
        email: "",
        telephone: "",
        username: "",
        pass: '',
        checkPass: '',
      },
      rules: {
          pass: [
            { validator: validatePass, trigger: 'blur' }
          ],
          checkPass: [
            { validator: validatePass2, trigger: 'blur' }
          ]
        }
    };
  },
  methods: {
    register(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          alert('submit!');
          // let email = this.registerForm.email
          // let telephone = this.registerForm.telephone
          // let username = this.registerForm.username
          // let pass = this.registerForm.pass
          // let checkPass = this.registerForm.checkPass
          // window.console.log(email, telephone)
          let param = {
            "email": this.registerForm.email,
            "telephone": this.registerForm.telephone,
            "username": this.registerForm.username,
            "pass": this.registerForm.pass,
            "checkPass": this.registerForm.checkPass,
          }
          this.$axios({
            method: 'post',
            url: 'http://127.0.0.1:8000/user/register',
            data: param
          }).then((response) => {
            this.$message({
                  message: '注册成功',
                  type: 'success'
                });
            window.console.log(response.data)
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