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
          <admin_entries v-if="index == 0"></admin_entries>
          <admin_review v-if="index == 1"></admin_review>
        </a-layout-content>
      </a-layout>
    </a-layout>
</template>

<script>
import admin_entries from '~/components/admin_entries.vue'
import admin_review from '~/components/admin_review.vue'

export default {
  components: {
    admin_entries,
    admin_review
  },
  data() {
    return {
        index: 0
    }
  },
  async asyncData({ store, redirect }) {
    if (!store.state.isLogin) {
      redirect('/')
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
