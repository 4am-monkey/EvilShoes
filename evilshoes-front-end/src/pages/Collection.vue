<template>
  <div class="x-collection">
    <!-- 收藏夹 -->
    <!-- 测试AJAX发送的数据 -->
    <!-- <el-button @click="getcollections">获取收藏的数据</el-button> -->
    <el-table :data="favourites" style="width: 100%" highlight-current-row>
      <el-table-column label="商品图片" width="250">
        <template slot-scope="scope">
          <img
            :src="scope.row.img"
            :alt="scope.row.img"
            width="150"
            @click="toDetals(scope.row.c_id)"
          />
        </template>
      </el-table-column>
      <el-table-column prop="name" label="名称" width="300"></el-table-column>
      <el-table-column prop="price" label="价格" width="300"></el-table-column>
      <el-table-column label="操作" width="300">
        <template slot-scope="scope">
          <el-button size="mini" type="danger" @click="handleDelete(scope.row.c_id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
<script>
export default {
  name: "x-collection",
  data() {
    return {
      favourites: []
    };
  },
  created() {
    this.getcollections();
  },
  methods: {
    getcollections() {
      var AUTH_TOKEN = window.localStorage.getItem("evil_token");
      this.$axios({
        method: "get",
        url: "http://127.0.0.1:8000/favourite/",
        headers: {
          Authorization: AUTH_TOKEN
        }
      })
        .then(res => {
          // window.console.log(res.data.data);
          let favs = JSON.parse(res.data.data); // 将JSON字符串解析为JSON对象
          // window.console.log(favs[0].fields)
          // window.console.log(favs)
          // 过滤信息
          for (var i = 0; i < favs.length; i++) {
            let fav = {};
            fav.c_id = favs[i].pk;
            fav.name = favs[i].fields.name;
            fav.img = "http://127.0.0.1:8000/media/" + favs[i].fields.images;
            fav.price = "￥" + favs[i].fields.price;
            this.favourites.push(fav);
          }
          //   window.console.log(this.favourites)
        })
        .catch(err => {
          window.console.log(err);
        });
    },
    handleDelete(id) {
      var AUTH_TOKEN = window.localStorage.getItem("evil_token");
      var params = { commodity_id: id };
      this.$axios({
        method: "delete",
        url: "http://127.0.0.1:8000/favourite",
        headers: { Authorization: AUTH_TOKEN },
        data: params
      }).then(res => {
        if (res.data.code == 200) {
          this.favourites = [];
          this.getcollections();
          this.$message({
            type: "success",
            message: "删除成功"
          });
        }else{
            window.console.log('删除失败')
        }
      });
    },
    toDetals(id) {
      this.$router.push({ path: "/details/" + id });
    }
  }
};
</script>
<style scoped>
element.style {
  width: 1200px;
}
img:hover {
  cursor: pointer;
}
</style>