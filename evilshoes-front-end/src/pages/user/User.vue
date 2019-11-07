<template>
    <div class="x-user">
        圣诞节
    </div>
</template>

<script>
export default {
    name: 'x-user',
    mounted(){
        var AUTH_TOKEN = window.localStorage.getItem("evil_token");
        this.$axios({
          method: "get",
          url: "http://127.0.0.1:8000/user/info",
          headers: { Authorization: AUTH_TOKEN }
        }).then(response => {
          window.console.log(response.data);
          if (response.data.code == 200) {
            // this.commodity = response.data.data;
          } else {
            this.$router.push({ path: '/'})
            this.$message.error('请登录');
          }
        });
    },
}
</script>

<style>
.x-user{
    border: solid 1px red;
}
</style>