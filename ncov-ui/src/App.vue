<template>
  <div id="app">
    <div class="customize">
      <router-view />
    </div>
    <van-tabbar v-model="active" @change="onTabChange">
      <van-tabbar-item name="home" to="/" icon="location-o">分布</van-tabbar-item>
      <van-tabbar-item name="trend" to="/trend" icon="chart-trending-o">趋势</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script>
export default {
  data() {
    return {
      active: "home"
    };
  },
  methods:{
    onTabChange(){

    }
  }
};
</script>
<style lang="scss">
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
.customize{
  margin-bottom: 100px;
}
</style>
