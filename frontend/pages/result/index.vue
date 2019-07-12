<template>
  <div class="container text-center">
      <a-spin :spinning="spinning">
        <a-form
            :form="form"
            @submit="search"
            layout="inline"
            class="text-left"
        >
            <a-form-item label="关键字">
            <a-input
                v-decorator="[
                'keyword',
                {
                    rules: [{ required: true, message: '请输入搜索关键字' }],
                }
                ]"
                placeholder="请输入搜索关键字"
            />
            </a-form-item>
            <a-form-item>
            <a-button type="primary" html-type="submit">搜索</a-button>
            </a-form-item>
            <a-form-item>
            <a-button>高级搜索</a-button>
            </a-form-item>
        </a-form>
        <a-table
            :columns="columns"
            :dataSource="result"
            :rowKey="result => result.id"
            :bordered="true"
            class="table"
        >
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
        form: this.$form.createForm(this),
        columns: [{
            title: '中文(简体)',
            dataIndex: 'SimplifiedName',
            key: 'SimplifiedName',
        }, {
            title: '中文(繁体)',
            dataIndex: 'TraditionalName',
            key: 'TraditionalName',
        }, {
            title: '拼音',
            dataIndex: 'PinyinName',
            key: 'PinyinName',
        }, {
            title: '英文_1',
            dataIndex: 'EnglishName_1',
            key: 'EnglishName_1',
        }, {
            title: '英文_2',
            dataIndex: 'EnglishName_2',
            key: 'EnglishName_2',
        }, {
            title: '英文_3',
            dataIndex: 'EnglishName_3',
            key: 'EnglishName_3',
        }, {
            title: '英文释义',
            dataIndex: 'EnglishInterpretation',
            key: 'EnglishInterpretation',
        }, , {
            title: '所属分类',
            dataIndex: 'sortName',
            key: 'sortName',
        }, , {
            title: '分类代码',
            dataIndex: 'sortCode',
            key: 'sortCode',
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
      search(e) {
          e.preventDefault()
          this.spinning = true
          this.form.validateFields((err, values) => {
              if (!err) {
              this.$axios.post('search', qs.stringify({
                  keyword: values.keyword
              }))
              .then((res) => {
                  this.spinning = false
                  this.result = res.data.info
              })
            }
        })
      }
  }
}
</script>

<style scoped>
.table {
    background-color: white;
}
.table >>> .ant-pagination {
    margin: 16px auto;
    float: none;
}

@media screen and (min-width: 1200px) {
    .container {
        width: 1600px;
    }
}
</style>
