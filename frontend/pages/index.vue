<template>
  <div  class="container text-center">
    <h1>中医中英术语查询系统</h1>
    <a-spin :spinning="spinning">
      <a-form
        :form="form"
        @submit="search"
        layout="inline"
        class="form"
      >
        <!--
        <a-form-item label="搜索字段" v-bind="formItemLayout">
          <a-select
            v-decorator="[
              'field',
              {
                initialValue: '中文(简体)'
              }
            ]"
          >
            <a-select-option value="中文(简体)">中文(简体)</a-select-option>
            <a-select-option value="中文(繁体)">中文(繁体)</a-select-option>
            <a-select-option value="拼音">拼音</a-select-option>
          </a-select>
        </a-form-item>
        -->
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
      form: this.$form.createForm(this),
      formItemLayout: {
        labelCol: {
          xs: { span: 24 },
          sm: { span: 7 },
        },
        wrapperCol: {
          xs: { span: 24 },
          sm: { span: 11 },
        },
      },
      tailFormItemLayout: {
        wrapperCol: {
          xs: { span: 24 },
          sm: { span: 16, offset: 4 },
        },
      }
    }
  },

  methods: {
    ...mapMutations({
      setSearchResult: 'setSearchResult'
    }),

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
            this.setSearchResult(res.data.info)
            this.$router.push({ path: '/result' })
          })
        }
      })
    }
  }
}
</script>

<style scoped>
.form {
  margin-top: 30px;
}
</style>
