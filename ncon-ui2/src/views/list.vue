<template>
  <div class="mainPage">
    <tabBar :activeIndex="activeIndex" :list="tabList"></tabBar>
    <div class="search b-border">
      <input type="text" placeholder="请搜索关键字" v-model.trim="keyword">
    </div>
     <div class="list">
      <scroller ref="scroller" class="my-scroller" :on-refresh="refresh" :on-infinite="infinite" noDataText="已无更多数据">
        <div class="listItem" v-for="(item,index) in list" :key="index">
          <span>这是一行数据{{index+1}}</span>
        </div>
      </scroller>
    </div>
  </div>
</template>

<script>
import tabBar from '../components/tabBar'
export default {
  components: { tabBar },
  data () {
    return {
      keyword: '',
      activeIndex: 0,
      tabList: [
        { name: '我接收的', url: '/list' },
        { name: '我发起的', url: '/error' }
      ],
      params: {
        pageNum: 0,
        pageSize: 20
      },
      list: []
    }
  },
  methods: {
    refresh (done) {
      this.list = []
      this.params.pageNum = 1
      this.getList(done)
    },
    infinite (done) {
      if (this.list.length > 25) {
        this.$refs.scroller.finishInfinite(true)
        if (this.list.length < 10) {
          document.getElementsByClassName('loading-layer')[0].style.display = 'none'
        }
        document.getElementsByClassName('pull-to-refresh-layer')[0].style.display = 'none'
      } else {
        this.params.pageNum++
        this.getList(done)
      }
    },
    getList (done) {
      document.getElementsByClassName('pull-to-refresh-layer')[0].style.display = 'block'
      for (let i = 0; i < 10; i++) {
        this.list.push({id: i + 1})
      }
      done && done()
    }
  }
}
</script>

<style scoped lang="less">
.mainPage{
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
.list{
  height: calc(100% - 105px);
  background-color: #fff;
  position: relative;
}
.listItem{
height: 45px;
line-height: 45px;
font-size: 16px;
padding:0 15px;
}
</style>
