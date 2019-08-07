<template>
  <div class="container">
    <div class="warpper text-center">
        <div class="login">
            <a-form :form="form_login" @submit="login">
                <a-form-item label="用户名" :label-col="{ span: 5 }" :wrapper-col="{ span: 18 }">
                    <a-input v-decorator="[
                        'email',
                        { rules: [{ required: true, message: '请输入邮箱'}] }
                    ]"
                    placeholder="请输入邮箱">
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
                    <a-button type="primary" html-type="submit" style="width: 100%">登录</a-button>
                </a-form-item>
            </a-form>
        </div>
    </div>
  </div>
</template>

<script>
import qs from "qs"

export default {
    name: "Login",
    data() {
        return {
            form_login: this.$form.createForm(this)
        }
    },
    methods: {
        login(e) {
            e.preventDefault()
            this.form_login.validateFields((err, values) => {
                if (!err) {
                    this.$axios.post('login', qs.stringify({
                        email: values.email,
                        password: md5(values.password)
                    }))
                    .then((response) => {
                        if (response.data == 1) {
                        this.$message.error('用户名不存在')
                        }
                        else if (response.data == 2) {
                        this.$message.error('密码错误')
                        } 
                        else {
                        this.$router.push({ path: '/' })
                        }
                    })
                }
            })
        },
        sendSMS() {

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
