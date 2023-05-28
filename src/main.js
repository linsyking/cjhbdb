import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import Antd from "ant-design-vue"
import "ant-design-vue/dist/antd.css"
import { createRouter, createWebHashHistory } from 'vue-router'
import Main from './components/Main.vue'

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        { path: '/', redirect: '/main' },
        { path: '/main', component: Main },
    ],
})

createApp(App)
    .use(Antd)
    .use(router)
    .mount('#app')
