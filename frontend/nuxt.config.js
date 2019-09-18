
export default {
  mode: 'universal',
  /*
  ** Headers of the page
  */
  head: {
    title: '中医术语中英对照查询系统(The System for Chinese-English Terminology of Chinese Medicine)',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '中医术语中英对照查询系统, The System for Chinese-English Terminology of Chinese Medicine' },
      { hid: 'keywords', name: 'keywords', content: '湖南中医药大学, HNUCM, 中医, 术语, 对照查询系统, 中英, Chinese Medicine, Terminology, Chinese-English' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ],
    script: [
      { src: 'https://hm.baidu.com/hm.js?9c41b8533fc99752e58099797ce4cf87' }
    ]
  },
  /*
  ** Customize the progress-bar color
  */
  loading: { color: '#fff' },
  /*
  ** Global CSS
  */
  css: [
    'ant-design-vue/dist/antd.css',
    '~assets/css/bootstrap.min.css',
    '~assets/css/style.css'
  ],
  /*
  ** Plugins to load before mounting the App
  */
  plugins: [
    '@/plugins/antd-ui',
    { src: '~/plugins/bdtj.js', ssr: false }
  ],
  /*
  ** Nuxt.js modules
  */
  modules: [
    '@nuxtjs/axios'
  ],
  /*
  ** Axios module configuration
  */
 axios: {
    proxy: true,
    prefix: '/api'
  },
  proxy: {
    '/api': { 
      target: 'http://localhost:8000',
      pathRewrite: {
        '^/api': '/api',
        changeOrigin: true
      }
    }
  },
  /*
  ** Build configuration
  */
  build: {
    /*
    ** You can extend webpack config here
    */
    extend(config, ctx) {
    }
  }
}
