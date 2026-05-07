import { createApp } from 'vue'

import App from './App.vue'
import { hydrateAuth } from './lib/auth'
import router from './router'
import './style.css'

await hydrateAuth()

createApp(App).use(router).mount('#app')
