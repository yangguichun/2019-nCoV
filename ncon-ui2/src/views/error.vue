<template>
  <div class="mainPage">
    <tabBar :activeIndex="activeIndex" :list="tabList"></tabBar>
    <div class="search b-border">
      <input type="text" placeholder="请搜索关键字" v-model.trim="keyword">
    </div>
    <div class="list">
      <noData txt="暂无收到的消息"></noData>
    </div>
  </div>
</template>

<script>
import noData from '../components/noData'
import tabBar from '../components/tabBar'
export default {
  name: 'empty',
  components: { noData, tabBar },
  data () {
    return {
      keyword: '',
      activeIndex: 1,
      tabList: [
        { name: '我接收的', url: '/list' },
        { name: '我发起的', url: '/error' }
      ]
    }
  },
  methods: {
    toSearch () {
      console.log('搜索')
    },
    cancelSearch () {
      console.log('取消搜索')
    }
  }
}
</script>

<style scoped lang="less">
.mainPage {
  height: 100%;
  background-color: #fff;
}
.search {
  padding: 10px 15px;
  position: relative;
  input {
    width: 100%;
    height: 40px;
    border-radius: 4px;
    font-size: 14px;
    padding: 0 10px;
    background: rgba(245, 246, 248, 1);
    border-radius: 4px;
  }
}
.list {
  height: calc(100% - 105px);
  background-color: #fff;
  position: relative;
}
</style>
