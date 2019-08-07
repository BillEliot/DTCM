<template>
    <a-layout class="wapper">
      <!-- sider -->
      <a-layout-sider>
          <a-menu
            mode="inline"
            theme="dark"
            style="height: 100%"
        >
            <a-sub-menu key="database">
                <span slot="title"><a-icon type="database" /><span>CMS</span></span>
                <a-menu-item key="entry:1" @click="index = 0">全部术语</a-menu-item>
                <a-menu-item key="entry:2" @click="index = 1">待审核术语</a-menu-item>
            </a-sub-menu>
        </a-menu>
      </a-layout-sider>
      <a-layout>
        <!-- content -->
        <a-layout-content>

        </a-layout-content>
      </a-layout>
    </a-layout>
</template>

<script>
import qs from 'qs'

export default {
  components: {
  },
  data() {
    return {
        index: 0
    }
  },
  async asyncData({ $axios, redirect }) {

    return {
    }
  },
  methods: {
  }
}
</script>

<style scoped>
a {
    text-decoration: none;
}

.wapper {
    position: absolute;
    height: 100%;
    width: 100%;
}
</style>
