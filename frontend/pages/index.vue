<template>
  <div>
    <!-- Captcha -->
    <a-modal
        title="输入验证码(区分大小写)"
        :visible="visible"
        @ok="confirmCaptcha"
        @cancel="visible = false"
        :confirmLoading="confirmLoading"
    >
        <img :src="'/media/captchas/' + encryCaptcha.replace('/', '+') + '.jpg'">
        <a-input placeholder="请输入验证码" v-model="captcha">
            <a-icon slot="prefix" type="code" />
        </a-input>
    </a-modal>
    <div class="container text-center warpper">
      <img src="~assets/image/bg.png" class="logo" />
      <h1>中医术语中英对照查询系统</h1>
      <p class="sub-title">The System for Chinese-English Terminology of Chinese Medicine</p>
      <a-spin :spinning="spinning">
        <a-select v-model="rule" size="large" class="rule">
          <a-select-option value="中 -> 英">中(CN) -> 英(EN)</a-select-option>
          <a-select-option value="英 -> 中">英(EN) -> 中(CN)</a-select-option>
        </a-select>
        <a-auto-complete
          v-model="keyword"
          :dataSource="completeResult"
          size="large"
          @search="autoComplete"
          placeholder="输入关键字"
          :allowClear="true"
          class="auto-complete"
        />
        <a-button type="primary" @click="search" size="large" class="search">搜索</a-button>
      </a-spin>
    </div>
  </div>
</template>

<script>
import qs from 'qs'
import { mapMutations } from 'vuex'

export default {
  data() {
    return {
      spinning: false,
      keyword: '',
      rule: '中 -> 英',
      completeResult: [],
      captcha: '',
      encryCaptcha: '',
      visible: false,
      confirmLoading: false
    }
  },

  methods: {
    ...mapMutations({
      setSearchResult: 'setSearchResult'
    }),

    search() {
      this.spinning = true
      if (!!this.keyword) {
        this.$axios.post('search', qs.stringify({
          keyword: this.keyword,
          rule: this.rule,
          captcha: this.captcha,
          encryCaptcha: this.encryCaptcha
        }))
        .then((res) => {
          this.spinning = false
          this.confirmLoading = false
          if (res.data.encryCaptcha) {
            // Need to enter Captcha
            this.encryCaptcha = res.data.encryCaptcha
            this.visible = true
          }
          else if (res.data == 1) {
            this.$message.error('验证码错误')
          }
          else {
            this.setSearchResult(res.data.info)
            this.$router.push({ path: '/result' })
          }
        })
      }
      else {
        this.$message.error('输入些关键字吧～')
      }
    },
    confirmCaptcha() {
      if (!!this.captcha) {
          this.search()
      }
      else {
          this.$message.error('验证码不能为空')
      }
    },
    autoComplete(value) {
      this.$axios.post('autoComplete', qs.stringify({
        keyword: value,
        rule: this.rule
      }))
      .then((res) => {
        this.completeResult = res.data.info
      })
    }
  }
}
</script>

<style scoped>
.submit {
  margin-top: 10px;
  margin-right: 10px;
}

.warpper {
  margin-top: 50px;
}

.logo {
  width: 200px;
  height: 200px;
}

.sub-title {
  color: gray;
  font-size: 18px;
}

.auto-complete {
  width: 600px;
  height: 40px;
  margin-left: 10px;
}

.rule {
  width: 180px;
}

.search {
  margin-left: 10px;
}

@media screen and (max-width: 768px) {
  .auto-complete {
    width: 100px;
  }
}
@media screen and (max-width: 970px) {
  .auto-complete {
    width: 250px;
  }

  .rule {
    margin-bottom: 10px;
  }
}
</style>
