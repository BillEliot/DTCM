<template>
  <div class="container entry text-center">
    <img src="~assets/image/bg.png" class="logo" />
    <div class="row">
      <div class="col-md-4">
        <a-card title="中文(简体)">
          <p>{{ entry.SimplifiedName }}</p>
        </a-card>
      </div>
      <div class="col-md-4">
        <a-card title="中文(繁体)">
          <p>{{ entry.TraditionalName }}</p>
        </a-card> 
      </div>
      <div class="col-md-4">
        <a-card title="拼音">
          <p>{{ entry.PinyinName }}</p>
        </a-card>
      </div>
    </div>
    <hr />
    <div class="row">
      <div class="col-md-4">
        <a-card title="英文_1">
          <p>{{ entry.English_1 }}</p>
        </a-card>
      </div>
      <div class="col-md-4">
        <a-card title="英文_2">
          <p>{{ entry.English_2 }}</p>
        </a-card>
      </div>
      <div class="col-md-4">
        <a-card title="英文_3">
          <p>{{ entry.English_3 }}</p>
        </a-card>
      </div>
    </div>
    <hr />
    <div class="row">
      <div class="col-md-4">
        <a-card title="英文释义">
          <p>{{ entry.EnglishInterpretation }}</p>
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
</template>

<script>
import qs from 'qs'

export default {
  data() {
    return {
    }
  },

  async asyncData({ query, $axios, error }) {
    let entry = null

    await $axios.post('detail', qs.stringify({
      SimplifiedName: query.SimplifiedName
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
  width: 300px;
  height: 300px;
  margin-bottom: 30px;
}
</style>
