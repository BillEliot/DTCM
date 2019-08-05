<template>
  <div  class="container text-center warpper">
    <img src="~assets/image/bg.png" class="logo" />
    <h1>中医术语中英对照查询系统</h1>
    <p class="sub-title">A System for Chinese-English Terminology of Chinese Medicine</p>
    <a-spin :spinning="spinning">
      <a-select v-model="rule" class="rule">
        <a-select-option value="中 -> 英">中 -> 英</a-select-option>
        <a-select-option value="英 -> 中">英 -> 中</a-select-option>
      </a-select>
      <a-auto-complete
        v-model="keyword"
        :dataSource="completeResult"
        @search="autoComplete"
        placeholder="输入关键字"
        :allowClear="true"
        class="auto-complete"
      />
      <a-button type="primary" @click="search" style="margin-left: 10px">搜索</a-button>
    </a-spin>
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
          rule: this.rule
        }))
        .then((res) => {
          this.spinning = false
          this.setSearchResult(res.data.info)
          this.$router.push({ path: '/result' })
        })
      }
      else {
        this.$message.error('输入些关键字吧～')
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
.warpper {
  margin-top: 50px;
}

.logo {
  width: 300px;
  height: 300px;
}

.sub-title {
  color: lightgray;
  font-size: 18px;
}

.auto-complete {
  width: 600px;
  margin-left: 10px
}

.rule {
  width: 100px
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
