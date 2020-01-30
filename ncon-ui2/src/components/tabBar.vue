<template>
  <div class="tabBar clearfix">
    <div class="item" :class="{'active':activeIndex==index}" v-for="(item,index) in list" :key="index" @click="toUrl(item)">{{item.name}}</div>
  </div>
</template>

<script>
export default {
  props: {
    activeIndex: {
      type: Number
    },
    list: {
      type: Array
    }
  },
  methods: {
    toUrl (item) {
      this.$router.replace({
        path: item.url
      })
    }
  }
}
</script>

<style scoped lang="less">
.tabBar {
  // position: fixed;
  // top: 0px;
  width: 100%;
  height: 45px;
  line-height: 45px;
  padding: 0 15px;
  background-color: #fff;
  z-index: 99;
  .item {
    width: 50%;
    text-align: center;
    float: left;
    font-size: 16px;
  }
  .active {
    height: 44px;
    color: #597ef7;
    border-bottom: 3px solid #597ef7;
  }
}
</style>
