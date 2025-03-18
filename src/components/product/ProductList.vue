<template>
  <div class="product-list">
    <product-header
      :total-items="totalItems"
      v-model:sort-by="sortBy"
      :sort-options="sortOptions"
    />
    
    <product-items
      :items="items"
    />

    <product-pagination
      v-model:page="page"
      :total-pages="totalPages"
    />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import pusbub from 'pubsub-js'
import ProductHeader from './ProductHeader.vue'
import ProductItems from './ProductItems.vue'
import ProductPagination from './ProductPagination.vue'
import tempPng from '@/assets/test/1.png'

const sortBy = ref('newest')
const page = ref(1)
const totalPages = ref(10)
const totalItems = ref(100)

const sortOptions = [
  { title: '最新', value: 'newest' },
  { title: '最热', value: 'popular' },
  { title: '价格升序', value: 'price_asc' },
  { title: '价格降序', value: 'price_desc' }
]

// 示例数据
const items = ref([])

onMounted(() => {
    pusbub.subscribe('getData',(_, data) =>{
        items.value = data
    })
})

</script> 