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
                    :pagination="false"
                    class="table"
                >
                    <router-link
                        slot="SimplifiedName"
                        slot-scope="text, record"
                        target="_blank"
                        :to="{ path: '/result/Detail', query: { id: record.id } }"
                    >
                        {{ text }}
                    </router-link>
                    <router-link
                        slot="TraditionalName"
                        slot-scope="text, record"
                        target="_blank"
                        :to="{ path: '/result/Detail', query: { id: record.id } }"
                    >
                        {{ text }}
                    </router-link>
                </a-table>
            </a-spin>
        </div>
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
            scopedSlots: { customRender: 'SimplifiedName' }
        },{
            title: '中文(繁體)',
            dataIndex: 'TraditionalName',
            scopedSlots: { customRender: 'TraditionalName' }
        }, {
            title: '拼音',
            dataIndex: 'PinyinName',
        }, {
            title: 'WHO',
            dataIndex: 'EnglishName_1',
        }],
        captcha: '',
        encryCaptcha: '',
        visible: false,
        confirmLoading: false
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
        if (!!this.keyword) {
            this.spinning = true
            this.confirmLoading = true
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
                    this.visible = false
                    this.result = res.data.info
                    this.captcha = ''
                    this.encryCaptcha = ''
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
