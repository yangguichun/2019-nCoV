<template>
  <div>
    <div class="btn" :class="{'footer':isBottom}" v-if="count==1">
      <button class="button" :class="{'o8':loading,'round':round,'simple':simple}" @click="submit" :disabled="loading">
        <img src="../assets/img/ring.png" alt="" width="20" class="loading" v-if="loading && !simple">
        <img src="../assets/img/color_loading1.png" alt="" width="20" class="loading" v-if="loading && simple">
        <span>{{txt}}</span>
      </button>
    </div>
    <div class="footerBtn2" v-if="count==2">
      <button class="btnLeft" @click="onLeft">{{leftTxt}}</button>
      <button class="btnRight" @click="onRight">{{rightTxt}}</button>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      // txt: '提交'
    }
  },
  props: {
    txt: {
      type: String
    },
    count: {
      type: Number,
      default: 1
    },
    rightTxt: {
      type: String
    },
    leftTxt: {
      type: String
    },
    loading: {
      type: Boolean,
      default: false
    },
    isBottom: {
      type: Boolean,
      default: true
    },
    round: {
      type: Boolean,
      default: false
    },
    simple: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    submit () {
      this.$emit('onSubmit', '')
    },
    onLeft () {
      this.$emit('onLeft', '')
    },
    onRight () {
      this.$emit('onRight', '')
    }
  }
}
</script>

<style scoped lang="less">
.btn {
  width: 100%;
  height: 65px;
  padding: 10px 15px;
  font-size: 16px;
  background-color: #fff;
  // position: fixed;
  // top: 0;
}
.footer {
  bottom: 0;
  left: 0;
  position: fixed;
}
.button {
  width: 100%;
  height: 45px;
  line-height: 45px;
  background-color:#597EF7;
  color: white;
  text-align: center;
  border-radius: 4px;
  font-size: 16px;
  > img {
    width: 20px;
    vertical-align:middle;
  }
}
.footerBtn2 {
  bottom: 0;
  left: 0;
  width: 100%;
  height: 65px;
  position: fixed;
  font-size: 16px;
  padding: 10px 15px;
  button {
    width: 48%;
    height: 45px;
    display: block;
    float: left;
    line-height: 45px;
    background-color: #597EF7;
    color: white;
    text-align: center;
    border-radius: 4px;
  }
  .btnLeft {
    margin-right: 4%;
  }
}
.round {
  border-radius: 45px !important;
}
.simple {
  border: 0.01rem solid #597EF7;
  background-color: #fff !important;
  color: #597EF7 !important;
}
.o8 {
  opacity: 0.8;
}
.loading {
  animation: rotate 0.7s linear infinite;
}
@keyframes rotate {
  0% {
    transform: rotate(0);
  }
  50% {
    transform: rotate(180deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
