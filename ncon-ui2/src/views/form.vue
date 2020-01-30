<template>
  <div class="mainPage">
    <div class="list">
      <div class="listItem clearfix b-border">
        <div class="item-left fl">
          <span class="require"> *</span>姓名</div>
        <div class="item-right fl">
          <input type="text" placeholder="请输入客户姓名" v-model="userName" maxlength="30">
        </div>
      </div>
      <div class="listItem clearfix b-border">
        <div class="item-left fl">
          手机号</div>
        <div class="item-right fl">
          <input type="text" placeholder="请输入手机号" v-model="telephone" maxlength="11">
        </div>
      </div>
      <div class="listItem clearfix b-border" @click="selectDate">
        <div class="item-left fl">生日</div>
        <div class="item-right fl">
          <input type="text" placeholder="请选择生日" v-model="birthday" readonly>
        </div>
      </div>
      <div class="listItem clearfix b-border" @click="show1=true">
        <div class="item-left fl">会员卡</div>
        <div class="item-right fl">
          <input type="text" placeholder="请选择会员卡" v-model="cardName" readonly>
        </div>
      </div>
    </div>
    <actionsheet v-model="show1" :menus="cardList" :close-on-clicking-mask="false" show-cancel @on-click-menu="selectCard"></actionsheet>
    <vButtom txt="提交" :isBottom="true" :loading="loading"  @onSubmit="onSubmit"></vButtom>
  </div>
</template>

<script>
import vButtom from '../components/vButtom'
import Vue from 'vue'
import { Actionsheet, DatetimePlugin } from 'vux'
Vue.use(DatetimePlugin)
export default {
  components: { Actionsheet, vButtom },
  data () {
    return {
      userName: '',
      telephone: '',
      birthday: '',
      cardName: '',
      show1: false,
      cardList: ['储值卡', '计次卡'],
      loading: false
    }
  },
  methods: {
    selectDate (val) {
      let vm = this
      this.$vux.datetime.show({
        value: vm.birthday,
        cancelText: '取消',
        confirmText: '确定',
        format: 'YYYY-MM-DD',
        yearRow: '{value}年',
        monthRow: '{value}月',
        dayRow: '{value}日',
        startDate: '1900-01-01',
        onConfirm (val) {
          vm.birthday = val
        }
      })
    },
    selectCard (key, val) {
      this.cardName = val
    },
    onSubmit () {
      if (!this.userName) {
        this.$toast({msg: '请输入客户名字'})
        return
      }
      this.loading = true
      setTimeout(() => {
        this.loading = false
        this.$toast({msg: '提交成功', type: 'success'})
      }, 1000)
    }
  }
}
</script>

<style scoped lang="less">
.mainPage {
  height: 100%;
}
.list {
  background-color: #fff;
}
.list {
  margin-bottom: 10px;
  padding-left: 15px;
  background-color: #fff;
  .listItem {
    padding: 14px 0;
    padding-right: 15px;
    position: relative;
    .require {
      position: absolute;
      top: 15px;
      left: -8px;
      color: #f74640 !important;
    }
    .item-left {
      width: 27%;
      line-height: 22px;
    }
    .item-right {
      width: 73%;
      > input {
        max-width: 185px;
        line-height: 22px;
        -webkit-user-select: text !important;
        user-select: text !important;
        cursor: pointer;
      }
    }
    .item-top {
      margin-bottom: 14px;
    }
    .left {
      width: 105px;
      line-height: 21px;
    }
    .right {
      width: 240px;
      line-height: 21px;
    }
  }
}
</style>
