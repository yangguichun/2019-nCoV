<template>
  <div id="app">
    <van-tabbar v-model="active" @change="onTabChange">
      <van-tabbar-item name="home" to="/" icon="home-o">home</van-tabbar-item>
      <van-tabbar-item name="home2" to="/about" icon="setting-o">about</van-tabbar-item>
    </van-tabbar>
    <router-view />
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
</style>
