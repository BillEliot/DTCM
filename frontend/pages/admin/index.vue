<template>
  <div class="container">
    <div class="warpper">
        <a-spin :spinning="spinning">
            <div class="login">
                <a-form :form="form_login">
                    <a-form-item label="用户名" :label-col="{ span: 5 }" :wrapper-col="{ span: 18 }">
                        <a-input v-decorator="[
                            'username',
                            { rules: [{ required: true, message: '请输入用户名'}] }
                        ]"
                            placeholder="请输入用户名">
                            <a-icon slot="prefix" type="user" style="color:rgba(0,0,0,.25)" />
                        </a-input>
                    </a-form-item>
                    <a-form-item label="密码" :label-col="{ span: 5 }" :wrapper-col="{ span: 18 }">
                        <a-input v-decorator="[
                            'password',
                            { rules: [{ required: true, message: '请输入密码'}] }
                        ]"
                            type="password" 
                            placeholder="请输入密码">
                            <a-icon slot="prefix" type="lock" style="color:rgba(0,0,0,.25)" />
                        </a-input>
                    </a-form-item>
                    <a-form-item>
                        <a-button type="primary" style="width: 100%" @click="login">登录</a-button>
                    </a-form-item>
                </a-form>
            </div>
        </a-spin>
    </div>
  </div>
</template>

<script>
import qs from "qs"
import md5 from 'js-md5'
import { mapMutations } from 'vuex'

export default {
    name: "Login",
    data() {
        return {
            spinning: false,
            form_login: this.$form.createForm(this)
        }
    },
    methods: {
        ...mapMutations({
            setIsLogin: 'setIsLogin'
        }),

        login(e) {
            e.preventDefault()
            this.form_login.validateFields((err, values) => {
                if (!err) {
                    this.spinning = true
                    this.$axios.post('login', qs.stringify({
                        username: values.username,
                        password: md5(values.password)
                    }))
                    .then((response) => {
                        this.spinning = false
                        if (response.data == 1) {
                            this.$message.error('用户名或密码错误')
                        }
                        else {
                            this.setIsLogin(true)
                            this.$router.push({ path: '/admin/cms' })
                        }
                    })
                }
            })
        }
    }
}
</script>

<style scoped>
.warpper {
    width: 400px;
    margin: 0 auto;
    margin-top: 100px;
}

.login {
    border: 1px solid lightgray;
    padding: 20px;
}
</style>
