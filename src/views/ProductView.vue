<template>
  <div class="product-view">
    <sub-navigation />
    <v-container class="py-6">
      <v-row>
        <!-- 左侧筛选栏 -->
        <v-col cols="3">
          <product-filter @apply-filters="fetchSearchResults" />
        </v-col>
        <!-- 右侧产品列表 -->
        <v-col cols="9">
          <div v-if="loading" class="loading-container">
            <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
          </div>
          <div v-else>
            <product-list :items="searchResults" :total-items="totalItems" v-model:sort-by="sortBy" />
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import axios from 'axios'
import pubsub from 'pubsub-js'
import { VContainer, VRow, VCol, VProgressCircular } from 'vuetify/components'
import ProductList from '@/components/product/ProductList.vue'
import ProductFilter from '@/components/product/ProductFilter.vue'
import SubNavigation from '@/components/layout/SubNavigation.vue'

const searchQuery = ref('')
const searchResults = ref([])
const totalItems = ref(0)
const page = ref(1)
const sortBy = ref('newest')
const loading = ref(false)

const fetchSearchResults = async () => {
  loading.value = true
  try {
    const response = await axios.get('http://localhost:5000/api/search', {
      params: { q: searchQuery.value }
    })
    searchResults.value = response.data
    totalItems.value = searchResults.value.length
  } catch (error) {
    console.error('Error fetching search results:', error)
  } finally {
    loading.value = false
  }
}

// 监听搜索关键词变化
watch(searchQuery, fetchSearchResults, { immediate: false })

onMounted(() => {
    pubsub.subscribe('filter-loading',(_,data) => {
        loading.value = data
    })
})

</script>

<style lang="less" scoped>
.product-view {
  min-height: 100vh;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
</style>