<template>
  <div class="container text-center result">
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
    <a-table
        :columns="columns"
        :dataSource="result"
        :rowKey="result => result.id"
        :bordered="true"
        class="table"
    >
        <router-link
            slot="SimplifiedName"
            slot-scope="text"
            target="_blank"
            :to="{ path: '/result/Detail', query: { SimplifiedName: text } }"
        >
            {{ text }}
        </router-link>
    </a-table>
    </a-spin>
  </div>
</template>

<script>
import qs from 'qs'

export default {
  data() {
    return {
        spinning: false,
        keyword: '',
        rule: '中 -> 英',
        completeResult: [],
        columns: [{
            title: '中文(简体)',
            dataIndex: 'SimplifiedName',
            key: 'SimplifiedName',
            scopedSlots: { customRender: 'SimplifiedName' }
        }, {
            title: '拼音',
            dataIndex: 'PinyinName',
            key: 'PinyinName',
        }, {
            title: '英文_1',
            dataIndex: 'EnglishName_1',
            key: 'EnglishName_1',
        }]
    }
  },

  asyncData({ store }) {
      let result = store.state.searchResult

      return {
          result: result
      }
  },

  methods: {
      search() {
          this.spinning = true
          if (!!this.keyword) {
              this.$axios.post('search', qs.stringify({
                  keyword: this.keyword,
                  rule: this.rule
              }))
              .then((res) => {
                  this.spinning = false
                  this.result = res.data.info
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
a {
    text-decoration: none;
}

.result {
    margin-top: 100px;
}

.auto-complete {
  width: 600px;
  margin-left: 10px
}

.rule {
  width: 100px
}

.table {
    margin-top: 20px;
}
.table >>> .ant-pagination {
    margin: 16px auto;
    float: none;
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
