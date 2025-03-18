<template>
  <v-app>
    <app-header />
    <v-main>
      <router-view v-slot="{ Component }">
        <keep-alive>
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </v-main>
    <app-footer />
  </v-app>
</template>

<script setup>
import { VApp, VMain } from 'vuetify/components'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import { dataDecrypt, dataEncrypt } from './utils/crypto';
import axios from 'axios';
import api from './config/api';
import { onMounted } from 'vue';

// try to login using data
const autoLogin = async () => {
  const userInfo = localStorage.getItem('session_user')
  if (userInfo) {
    const { email, password } = JSON.parse(dataDecrypt(userInfo))
    const response = await axios.post(api.login, { email, password })
    if (response.data.success) {
      localStorage.setItem('token', response.data.data.token)
      localStorage.setItem('session_info', dataEncrypt(response.data.data.user))
    }
  }
}

onMounted(() => {
  autoLogin()
})
</script>

<style lang='less' scoped>

</style>