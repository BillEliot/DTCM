<template>
  <div>
    <!-- drawer_report -->
    <a-spin :spinning="spinning">
      <a-drawer
        title="报告错误"
        :width="360"
        @close="visible = false"
        :visible="visible"
        :wrapStyle="{ height: 'calc(100% - 10px)', overflow: 'auto', paddingBottom: '108px' }"
        style="z-index: 999"
      >
        <a-form :form="form" layout="vertical" hideRequiredMark>
          <a-form-item label="错误条目">
            <a-select
              v-decorator="[
                'item',
                {
                  initialValue: '中文(简体)'
                }
              ]"
            >
              <a-select-option value="中文(简体)">中文(简体)</a-select-option>
              <a-select-option value="中文(繁体)">中文(繁体)</a-select-option>
              <a-select-option value="拼音">拼音</a-select-option>
              <a-select-option value="英文_1">WHO</a-select-option>
              <a-select-option value="英文_2">PMPH</a-select-option>
              <a-select-option value="英文_3">WFCMS</a-select-option>
              <a-select-option value="英文释义">英文释义</a-select-option>
              <a-select-option value="分类名称">分类名称</a-select-option>
              <a-select-option value="分类代码">分类代码</a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="修改意见">
            <a-textarea
              v-decorator="['feedback', {
                rules: [{ required: true, message: '请输入修改意见' }]
              }]"
              placeholder="修改意见"
              :rows="8"
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
          style="z-index: 999"
        >
          <a-button
            :style="{ marginRight: '8px' }"
            @click="visible = false"
          >
            取消
          </a-button>
          <a-button @click="report" type="primary">提交</a-button>
        </div>
      </a-drawer>
    </a-spin>
    <!-- Captcha -->
    <a-modal
      title="输入验证码(区分大小写)"
      :visible="visible_captcha"
      @ok="confirmCaptcha"
      @cancel="visible_captcha = false"
      :confirmLoading="confirmLoading"
    >
      <img :src="'/media/captchas/' + encryCaptcha.replace('/', '+') + '.jpg'">
      <a-input placeholder="请输入验证码" v-model="captcha">
          <a-icon slot="prefix" type="code" />
      </a-input>
    </a-modal>
    <!-- end - drawer_report -->
    <div class="container entry text-center">
      <img src="~assets/image/bg.png" class="logo" />
      <br />
      <div class="text-left report">
        <a-button type="danger" @click="visible = true">报告错误</a-button>
      </div>
      <div class="row">
        <div class="col-md-4">
          <a-card title="中文(简体)">
            <p>{{ entry.simplifiedName }}</p>
          </a-card>
        </div>
        <div class="col-md-4">
          <a-card title="中文(繁体)">
            <p>{{ entry.traditionalName }}</p>
          </a-card> 
        </div>
        <div class="col-md-4">
          <a-card title="拼音">
            <p>{{ entry.pinyinName }}</p>
          </a-card>
        </div>
      </div>
      <hr />
      <div class="row">
        <div class="col-md-4">
          <a-card title="WHO">
            <p>{{ entry.englishName_1 }}</p>
          </a-card>
        </div>
        <div class="col-md-4">
          <a-card title="PMPH">
            <p>{{ entry.englishName_2 }}</p>
          </a-card>
        </div>
        <div class="col-md-4">
          <a-card title="WFCMS">
            <p>{{ entry.englishName_3 }}</p>
          </a-card>
        </div>
      </div>
      <hr />
      <div class="row">
        <div class="col-md-4">
          <a-card title="英文释义">
            <p>{{ entry.englishInterpretation }}</p>
          </a-card>
        </div>
        <div class="col-md-4">
          <a-card title="分类名称">
            <p>{{ entry.sortName }}</p>
          </a-card>
        </div>
        <div class="col-md-4">
          <a-card title="分类代码">
            <p>{{ entry.sortCode }}</p>
          </a-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import qs from 'qs'

export default {
  data() {
    return {
      form: this.$form.createForm(this),
      visible: false,
      spinning: false,
      confirmLoading: false,
      captcha: '',
      encryCaptcha: '',
      visible_captcha: false
    }
  },

  async asyncData({ query, $axios, error }) {
    let entry = null

    await $axios.post('detail', qs.stringify({
      id: query.id
    }))
    .then((res) => {
      if (res.data == 1) {
        error({ statusCode: 500, message: '未知错误' })
      }
      else {
        entry = res.data
      }
    })

    return {
      entry: entry
    }
  },

  methods: {
    report(e) {
      if (!!e) e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          this.spinning = true
          this.confirmLoading = true
          this.$axios.post('reportEntry', qs.stringify({
            id: this.entry.id,
            item: values.item,
            feedback: values.feedback,
            captcha: this.captcha,
            encryCaptcha: this.encryCaptcha
          }))
          .then((res) => {
            this.spinning = false
            this.confirmLoading = false
            if (res.data.encryCaptcha) {
              // Need to enter Captcha
              this.encryCaptcha = res.data.encryCaptcha
              this.visible_captcha = true
            }
            else if (res.data == 1) {
              this.$message.error('验证码错误')
            }
            else if (res.data == 2) {
              this.$message.error('未知错误')
            }
            else {
              this.spinning = false
              this.visible = false
              this.visible_captcha = false
              this.captcha = ''
              this.encryCaptcha = ''
              this.form.resetFields()
              this.$message.success('感谢您的提交，等待审核')
            }
          })
        }
      })
    },
    confirmCaptcha() {
      if (!!this.captcha) {
        this.report()
      }
      else {
        this.$message.error('验证码不能为空')
      }
    }
  }
}
</script>

<style scoped>
p {
  font-weight: bold;
  font-size: 18px;
}

.entry {
  margin-top: 20px;
  margin-bottom: 20px;
}

.logo {
  width: 200px;
  height: 200px;
  margin-bottom: 30px;
}

.report {
  margin-bottom: 10px;
}
</style>
