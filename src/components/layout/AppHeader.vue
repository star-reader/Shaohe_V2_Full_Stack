<template>
  <v-app-bar app color="primary" dark>
    <v-toolbar-title @click="goHome" class="clickable-title">微曦生物积木数据库</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn text to="/home">首页</v-btn>
    <v-btn text to="/product">产品</v-btn>
    <v-btn text to="/profile">个人中心</v-btn>
  </v-app-bar>
</template>

<script setup>
import { VAppBar, VToolbarTitle, VSpacer, VBtn } from 'vuetify/components'
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
  router.push('/home')
}
</script>

<style scoped>
.clickable-title {
  cursor: pointer;
}
</style>