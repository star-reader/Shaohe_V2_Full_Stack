<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'
import { VContainer, VRow, VCol } from 'vuetify/components'
import ProductCard from '@/components/product/ProductCard.vue'
import ProductFilter from '@/components/product/ProductFilter.vue'
import ProductHeader from '@/components/product/ProductHeader.vue'
import ProductPagination from '@/components/product/ProductPagination.vue'

const props = defineProps({
  query: String
})

const searchResults = ref([])
const totalItems = ref(0)
const page = ref(1)
const sortBy = ref('newest')

const fetchSearchResults = async () => {
  try {
    const response = await axios.get('http://localhost:3000/api/search', {
      params: { q: props.query }
    })
    searchResults.value = response.data
    totalItems.value = searchResults.value.length
  } catch (error) {
    console.error('Error fetching search results:', error)
  }
}

// 监听搜索关键词变化
watch(() => props.query, fetchSearchResults, { immediate: true })
</script>

<template>
  <div class="search-view">
    <v-container class="py-6">
      <v-row>
        <!-- 左侧筛选栏 -->
        <v-col cols="3">
          <product-filter />
        </v-col>
        
        <!-- 右侧搜索结果 -->
        <v-col cols="9">
          <product-header
            :total-items="totalItems"
            v-model:sort-by="sortBy"
            :sort-options="[
              { title: '最新', value: 'newest' },
              { title: '最热', value: 'popular' },
              { title: '相关度', value: 'relevance' }
            ]"
          />
          
          <!-- 搜索结果列表 -->
          <div v-if="searchResults.length > 0">
            <product-card
              v-for="item in searchResults"
              :key="item.id"
              :item="item"
            />
          </div>
          <div v-else class="text-center py-12">
            <p class="text-h6">未找到相关结果</p>
          </div>
          
          <!-- 分页 -->
          <product-pagination
            v-if="searchResults.length > 0"
            v-model:page="page"
            :total-pages="Math.ceil(totalItems / 10)"
          />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<style lang="less" scoped>
.search-view {
  min-height: 100vh;
  background-color: #f8f9fa;
}
</style> 