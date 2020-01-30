<template>
  <div>
    <div class="banner">
      <swiper :list="imgList" v-model="activeIndex" auto :show-dots="!showDots" dots-position="center"></swiper>
    </div>
    <div class="list clearfix">
      <div class="item fl" v-for="(item,index) in itemList" :key="index" @click="toUrl(index)">
        <img :src="item.icon" alt="">
        <div class="itemName">{{item.name}}</div>
      </div>
    </div>
    <footerBar></footerBar>
  </div>
</template>

<script>
import { Swiper } from 'vux'
import footerBar from '../components/footerBar'
export default {
  components: { Swiper, footerBar },
  data () {
    return {
      activeIndex: 0,
      showDots: false,
      imgList: [
        { img: require('../assets/img/banner/banner2.jpg') },
        { img: require('../assets/img/banner/banner1.jpg') },
        { img: require('../assets/img/banner/banner3.jpg') }
      ],
      itemList: [
        {name: '预约列表', url: '/list', icon: require('../assets/img/banner/item1.png')},
        {name: '填写表单', url: '/form', icon: require('../assets/img/banner/item2.png')},
        {name: '会员管理', url: '/', icon: require('../assets/img/banner/item3.png')},
        {name: '数据统计', url: '/', icon: require('../assets/img/banner/item1.png')},
        {name: '填写表单', url: '/', icon: require('../assets/img/banner/item2.png')},
        {name: '会员管理', url: '/', icon: require('../assets/img/banner/item3.png')},
        {name: '预约列表', url: '/', icon: require('../assets/img/banner/item1.png')},
        {name: '填写表单', url: '/', icon: require('../assets/img/banner/item2.png')},
        {name: '会员管理', url: '/', icon: require('../assets/img/banner/item3.png')},
        {name: '预约列表', url: '/', icon: require('../assets/img/banner/item1.png')},
        {name: '填写表单', url: '/', icon: require('../assets/img/banner/item2.png')},
        {name: '会员管理', url: '/', icon: require('../assets/img/banner/item3.png')}
      ]
    }
  },
  methods: {
    toUrl (index) {
      this.$router.push({
        path: this.itemList[index].url
      })
    }
  }
}
</script>

<style scoped lang="less">
.list {
  margin-top: 10px;
  background-color: #fff;
  padding: 15px;
  .item {
    width: 25%;
    text-align: center;
    margin-bottom: 15px;
    font-size: 14px;
    > img {
      width: 40px;
      margin-bottom: 6px;
    }
  }
}
</style>
