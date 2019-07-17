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
        <a-form-item :wrapper-col="{ span: 24 }">
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
      this.form.validateFields((err, values) => {
        if (!err) {
          this.spinning = true
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
