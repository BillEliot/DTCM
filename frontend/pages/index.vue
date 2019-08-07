<template>
  <div>
    <!-- drawer_submit -->
    <a-spin :spinning="spinning_submit">
      <a-drawer
        title="提交术语"
        :width="360"
        placement="left"
        @close="visible = false"
        :visible="visible"
        :wrapStyle="{ height: 'calc(100% - 108px)', overflow: 'auto', addingBottom: '108px' }"
      >
        <a-form :form="form" layout="vertical" hideRequiredMark>
          <a-form-item label="中文(简体)">
            <a-input
              v-decorator="['simplifiedName', {
                rules: [{ required: true, message: '请输入中文(简体)' }]
              }]"
              placeholder="中文(简体)"
            />
          </a-form-item>
          <a-form-item label="中文(繁体)">
            <a-input
              v-decorator="['traditionalName', {
                rules: [{ required: true, message: '请输入中文(繁体)' }]
              }]"
              placeholder="中文(繁体)"
            />
          </a-form-item>
          <a-form-item label="拼音">
            <a-input
              v-decorator="['pinyin', {
                rules: [{ required: true, message: '请输入拼音' }]
              }]"
              placeholder="拼音"
            />
          </a-form-item>
          <a-form-item label="英文_1">
            <a-input
              v-decorator="['englishName_1', {
                rules: [{ required: true, message: '请输入英文_1' }]
              }]"
              placeholder="英文_1"
            />
          </a-form-item>
          <a-form-item label="英文_2">
            <a-input
              v-decorator="['englishName_2']"
              placeholder="英文_2"
            />
          </a-form-item>
          <a-form-item label="英文_3">
            <a-input
              v-decorator="['englishName_3']"
              placeholder="英文_3"
            />
          </a-form-item>
          <a-form-item label="英文释义">
            <a-textarea
              v-decorator="['englishInterpretation', {
                rules: [{ required: true, message: '请输入英文释义' }]
              }]"
              placeholder="英文释义"
              :rows="4"
            />
          </a-form-item>
          <a-form-item label="分类名称">
            <a-input
              v-decorator="['sortName', {
                rules: [{ required: true, message: '请输入分类名称' }]
              }]"
              placeholder="分类名称"
            />
          </a-form-item>
          <a-form-item label="分类代码">
            <a-input
              v-decorator="['sortCode', {
                rules: [{ required: true, message: '请输入分类代码' }]
              }]"
              placeholder="分类代码"
            />
          </a-form-item>
        </a-form>
        <div
          :style="{
            position: 'absolute',
            left: 0,
            bottom: 0,
            width: '100%',
            borderTop: '1px solid #e9e9e9',
            padding: '10px 16px',
            background: '#fff',
            textAlign: 'right',
          }"
        >
          <a-button
            :style="{ marginRight: '8px' }"
            @click="visible = false"
          >
            取消
          </a-button>
          <a-button @click="submit" type="primary">提交</a-button>
        </div>
      </a-drawer>
    </a-spin>
    <!-- end drawer_submit -->
    <div class="text-right">
      <a-button type="primary" @click="visible = true" class="submit">提交术语</a-button>
    </div>
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
  </div>
</template>

<script>
import qs from 'qs'
import { mapMutations } from 'vuex'

export default {
  data() {
    return {
      spinning: false,
      spinning_submit: false,
      keyword: '',
      rule: '中 -> 英',
      completeResult: [],
      form: this.$form.createForm(this),
      visible: false
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
    submit(e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          this.spinning_submit = true
          this.$axios.post('submitEntry', qs.stringify({
            simplifiedName: values.simplifiedName,
            traditionalName: values.traditionalName,
            pinyin: values.pinyin,
            englishName_1: values.englishName_1,
            englishName_2: values.englishName_2,
            englishName_3: values.englishName_3,
            englishInterpretation: values.englishInterpretation,
            sortName: values.sortName,
            sortCode: values.sortCode
          }))
          .then((res) => {
            this.spinning = false
            if (res.data == 0) {
              this.$message.success('提交成功，等待审核')
              this.visible = false
            }
            else {
              this.$message.error('未知错误')
            }
          })
        }
      })
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
