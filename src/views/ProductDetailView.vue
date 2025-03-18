<template>
  <div class="product-detail" v-if="productData">
    <sub-navigation />
    
    <v-container>
      <!-- 面包屑导航 -->
      <detail-breadcrumb :item="productData" />
      
      <!-- 产品基本信息 -->
      <detail-header :item="productData" />
      
      <!-- 主要内容区域 -->
      <v-row>
        <!-- 左侧主要内容 -->
        <v-col cols="12" md="8">
          <detail-tabs :item="productData" />
        </v-col>
        
        <!-- 右侧信息栏 -->
        <v-col cols="12" md="4">
          <detail-sidebar :item="productData" />
        </v-col>
      </v-row>
    </v-container>
  </div>
  <div class="loading-container" v-else>
    <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { VContainer, VRow, VCol, VProgressCircular } from 'vuetify/components'
import SubNavigation from '@/components/layout/SubNavigation.vue'
import DetailBreadcrumb from '@/components/product-detail/DetailBreadcrumb.vue'
import DetailHeader from '@/components/product-detail/DetailHeader.vue'
import DetailTabs from '@/components/product-detail/DetailTabs.vue'
import DetailSidebar from '@/components/product-detail/DetailSidebar.vue'
import api from '@/config/api'

// 示例数据
const productData = ref(null)

onMounted(() => {
  const id = location.pathname.split('/')[2]
  if (location.search.includes('from=addgene')) {
    axios.get(`${api.getDetailedData}/${id}`).then(res => {
      productData.value = res.data.data
    })
  } else {
    axios.get(`${api.getTargetPlasmidData}/${id}`).then(res => {
      productData.value = res.data.data
    })
  }
})
</script>

<style lang="less" scoped>
.product-detail {
  background-color: #f8f9fa;
  min-height: 100vh;

  .v-container {
    padding-top: 24px;
    padding-bottom: 48px;
  }
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
</style>