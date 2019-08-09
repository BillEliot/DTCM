<template>
    <div>
        <!-- drawer -->
        <a-spin :spinning="spinning_entry">
            <a-drawer
                title="查看/修改术语"
                :width="360"
                @close="visible = false"
                :visible="visible"
            >
                <a-form :form="form" layout="vertical" hideRequiredMark>
                    <a-form-item label="简体中文">
                        <a-input
                            v-decorator="['simplifiedName', {
                                rules: [{ required: true, message: '请输入简体中文' }],
                            }]"
                            placeholder="简体中文"
                        />
                    </a-form-item>
                    <a-form-item label="繁体中文">
                        <a-input
                            v-decorator="['traditionalName']"
                            placeholder="繁体中文"
                        />
                    </a-form-item>
                    <a-form-item label="拼音">
                        <a-input
                            v-decorator="['pinyinName', {
                                rules: [{ required: true, message: '请输入拼音' }],
                            }]"
                            placeholder="拼音"
                        />
                    </a-form-item>
                    <a-form-item label="英文_1">
                        <a-input
                            v-decorator="['englishName_1', {
                                rules: [{ required: true, message: '请输入英文_1' }],
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
                            placeholder="英文_4"
                        />
                    </a-form-item>
                    <a-form-item label="英文释义">
                        <a-input
                            v-decorator="['englishInterpretation']"
                            placeholder="英文释义"
                        />
                    </a-form-item>
                    <a-form-item label="分类名称">
                        <a-input
                            v-decorator="['sortName', {
                                rules: [{ required: true, message: '请输入分类名称' }],
                            }]"
                            placeholder="分类名称"
                        />
                    </a-form-item>
                    <a-form-item label="分类代码">
                        <a-input
                            v-decorator="['sortCode', {
                                rules: [{ required: true, message: '请输入分类代码' }],
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
                    <a-button @click="update" type="primary">修改</a-button>
                </div>
            </a-drawer>
        </a-spin>
        <!-- end - drawer -->
        <a-spin :spinning="spinning">
            <div class="table-operations">
                <a-button @click="refresh">刷新</a-button>
            </div>
            <a-table :columns="columns" :dataSource="reviews">
                <span slot="action" slot-scope="record">
                    <a-button type="primary" @click="viewEntry(record.key)">查看/修改术语</a-button>
                    <a-divider type="vertical" />
                    <a-button type="danger" @click="deny(record.reviewID)">忽略</a-button>
                </span>
            </a-table>
        </a-spin>
    </div>
</template>

<script>
import qs from 'qs'

export default {
  data() {
    return {
        visible: false,
        spinning: false,
        spinning_entry: false,
        form: this.$form.createForm(this),
        entry: {},
        reviews: [],
        columns: [{
            title: '审核ID',
            dataIndex: 'reviewID',
            key: 'reviewID',
            sorter: (a, b) => a.reviewID - b.reviewID
        },
        {
            title: '术语ID',
            dataIndex: 'key',
            key: 'key',
            sorter: (a, b) => a.key - b.key
        },
        {
            title: '修改项目',
            dataIndex: 'item',
            key: 'item',
        }, 
        {
            title: '修改意见',
            dataIndex: 'feedback',
            key: 'feedback',
        },
        {
            title: '提交日期',
            dataIndex: 'date',
            key: 'date',
            sorter: (a, b) => a.date - b.date
        },
        {
            title: '操作',
            key: 'action',
            scopedSlots: { customRender: 'action' }
        }]
    }
  },
  async asyncData({ $axios, redirect }) {
    return {
    }
  },
  methods: {
      refresh() {
          this.spinning = true
          this.$axios.get('getAllReviews')
          .then((res) => {
              this.spinning = false
              this.reviews = res.data.info
          })
      },
      viewEntry(id) {
          this.visible = true
          this.spinning_entry = true
          this.$axios.post('getEntry', qs.stringify({
              id: id
          }))
          .then((res) => {
              this.spinning_entry = false
              if (res.data == 1) {
                  this.$message.error('未知错误')
                  this.visible = false
              }
              else {
                  this.entry = res.data
                  this.form.setFieldsValue({
                      simplifiedName: res.data.simplifiedName,
                      traditionalName: res.data.traditionalName,
                      pinyinName: res.data.pinyinName,
                      englishName_1: res.data.englishName_1,
                      englishName_2: res.data.englishName_2,
                      englishName_3: res.data.englishName_3,
                      englishInterpretation: res.data.englishInterpretation,
                      sortName: res.data.sortName,
                      sortCode: res.data.sortCode,
                  })
                  let reviews = [...this.reviews]
                  this.reviews = reviews.filter(item => item.key !== id)
              }
          })
      },
      deny(reviewID) {
          this.spinning = true
          this.$axios.post('denyReview', qs.stringify({
              reviewID: reviewID
          }))
          .then((res) => {
              if (res.data == 0) {
                  this.spinning = false
                  this.$message.success('已忽略')

                  let reviews = [...this.reviews]
                  this.reviews = reviews.filter(item => item.reviewID !== reviewID)
              }
              else {
                  this.$message.error('未知错误')
              }
          })
      },
      update(e) {
          e.preventDefault()
          this.form.validateFields((err, values) => {
            if (!err) {
                this.spinning_entry = true
                this.$axios.post('updateEntry', qs.stringify({
                    id: this.entry.id,
                    simplifiedName: values.simplifiedName,
                    traditionalName: values.traditionalName,
                    pinyinName: values.pinyinName,
                    englishName_1: values.englishName_1,
                    englishName_2: values.englishName_2,
                    englishName_3: values.englishName_3,
                    englishInterpretation: values.englishInterpretation,
                    sortName: values.sortName,
                    sortCode: values.sortCode
                }))
                .then((res) => {
                    if (res.data == 0) {
                        this.spinning_entry = false
                        this.visible = false
                        this.$message.success('修改成功')
                    }
                    else {
                        this.$message.error('未知错误')
                    }
                })
            }
        })
      }
  },
  mounted() {
      this.spinning = true
      this.$axios.get('getAllReviews')
      .then((res) => {
          this.spinning = false
          this.reviews = res.data.info
      })
  }
}
</script>

<style scoped>
a {
    text-decoration: none;
}

p {
    font-weight: bold;
    font-size: 18px;
}

.table-operations {
    margin: 15px;
}
</style>
