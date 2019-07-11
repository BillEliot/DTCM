<template>
  <div  class="container text-center">
    <h1>中医中英术语查询系统</h1>
    <a-form
      :form="form"
      @submit="submit"
      class="text-left form"
    >
      <a-form-item label="搜索字段" v-bind="formItemLayout">
        <a-select
          v-decorator="[
            'field',
            {
              initialValue: '中文(简体)'
            }
          ]"
        >
          <a-select-option value="中文(繁体)">中文(繁体)</a-select-option>
          <a-select-option value="拼音">拼音</a-select-option>
        </a-select>
      </a-form-item>
      <a-form-item label="关键字" v-bind="formItemLayout">
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
      <a-form-item v-bind="tailFormItemLayout">
        <a-button type="primary" html-type="submit" style="width: 100%">搜索</a-button>
      </a-form-item>
    </a-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
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
    submit() {

    }
  }
}
</script>

<style scoped>
.form {
  margin-top: 30px;
}
</style>
