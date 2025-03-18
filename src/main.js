import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import router from './router'
import { createVuetify } from 'vuetify'
import 'vuetify/styles'

const vuetify = createVuetify()

createApp(App)
  .use(router)
  .use(vuetify)
  .use(ElementPlus)
  .mount('#app')
