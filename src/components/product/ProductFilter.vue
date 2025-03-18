<template>
  <v-card class="filter-card">
    <v-card-title class="text-h6 py-4 px-4">筛选条件</v-card-title>
    <v-divider></v-divider>
    
    <!-- 搜索框 -->
    <div class="pa-4">
      <v-text-field
        v-model="searchQuery"
        label="搜索关键词"
        variant="outlined"
        density="comfortable"
        hide-details
        prepend-inner-icon="mdi-magnify"
        class="mb-4"
      ></v-text-field>
    </div>

    <!-- 数据源选择 -->
    <v-card-text class="pa-4">
      <div class="text-subtitle-2 mb-2">数据源选择</div>
      <div class="d-flex flex-wrap gap-2">
        <v-chip
          :color="searchMode === 'all' ? 'primary' : undefined"
          :variant="searchMode === 'all' ? 'flat' : 'outlined'"
          @click="searchMode = 'all'"
          class="cursor-pointer"
        >
          搜索所有来源
        </v-chip>
        <v-chip
          :color="searchMode === 'onlyDb' ? 'primary' : undefined"
          :variant="searchMode === 'onlyDb' ? 'flat' : 'outlined'"
          @click="searchMode = 'onlyDb'"
          class="cursor-pointer"
        >
          仅搜索数据库
        </v-chip>
        <v-chip
          :color="searchMode === 'allDb' ? 'primary' : undefined"
          :variant="searchMode === 'allDb' ? 'flat' : 'outlined'"
          @click="searchMode = 'allDb'"
          class="cursor-pointer"
        >
          查看所有数据库记录
        </v-chip>
      </div>
    </v-card-text>

    <!-- 筛选项 -->
    <v-list>
      <!-- 类型筛选 -->
      <v-list-group value="type">
        <template v-slot:activator="{ props }">
          <v-list-item v-bind="props" title="类型"></v-list-item>
        </template>
        <v-list-item v-for="type in types" :key="type">
          <template v-slot:default>
            <v-checkbox
              v-model="selectedTypes"
              :label="type"
              :value="type"
              hide-details
              density="compact"
            ></v-checkbox>
          </template>
        </v-list-item>
      </v-list-group>

      <!-- 分类筛选 -->
      <v-list-group value="category">
        <template v-slot:activator="{ props }">
          <v-list-item v-bind="props" title="分类"></v-list-item>
        </template>
        <v-list-item v-for="category in categories" :key="category">
          <template v-slot:default>
            <v-checkbox
              v-model="selectedCategories"
              :label="category"
              :value="category"
              hide-details
              density="compact"
            ></v-checkbox>
          </template>
        </v-list-item>
      </v-list-group>

      <!-- 物种系统筛选 -->
      <v-list-group value="species">
        <template v-slot:activator="{ props }">
          <v-list-item v-bind="props" title="物种系统"></v-list-item>
        </template>
        <v-list-item v-for="species in speciesList" :key="species">
          <template v-slot:default>
            <v-checkbox
              v-model="selectedSpecies"
              :label="species"
              :value="species"
              hide-details
              density="compact"
            ></v-checkbox>
          </template>
        </v-list-item>
      </v-list-group>
    </v-list>

    <!-- 应用/重置按钮 -->
    <div class="pa-4">
      <v-btn
        color="primary"
        block
        class="mb-2"
        @click="applyFilters"
      >
        应用筛选
      </v-btn>
      <v-btn
        variant="outlined"
        block
        @click="resetFilters"
      >
        重置
      </v-btn>
    </div>
  </v-card>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { 
  VCard, 
  VCardTitle, 
  VCardText,
  VDivider, 
  VTextField, 
  VList, 
  VListGroup, 
  VListItem, 
  VCheckbox, 
  VBtn,
  VChip
} from 'vuetify/components'
import api from '@/config/api'
import pubsub from 'pubsub-js'

const searchQuery = ref('')
const selectedTypes = ref([])
const selectedCategories = ref([])
const selectedSpecies = ref([])
const searchMode = ref('all') // 'all', 'onlyDb', 'allDb'

// 筛选选项数据
const types = ['质粒', '菌株', '感受态细胞', '细胞', '病毒']
const categories = ['基因编辑', 'CRISPR', 'Cre-lox', '同源重组']
const speciesList = ['微生物', '人', '动物', '植物']

// 搜索数据库
const searchDatabase = async (query) => {
  try {
    const response = await axios.get(`${api.searchPlasmidData}?query=${query}`)
    if (response.data.success) {
      pubsub.publish('filter-loading', false)
      return response.data.data
    }
    return []
  } catch (error) {
    console.error('搜索数据库失败:', error)
    return []
  }
}

// 获取所有数据库记录
const getAllDatabaseRecords = async () => {
  try {
    const response = await axios.get(api.getAllPlasmidData)
    if (response.data.success) {
      pubsub.publish('filter-loading', false)
      return response.data.data.plasmids
    }
    return []
  } catch (error) {
    console.error('获取数据库记录失败:', error)
    return []
  }
}

// 应用筛选
const applyFilters = async () => {
  let results = []
  pubsub.publish('filter-loading', true)

  switch (searchMode.value) {
    case 'onlyDb':
      // 仅搜索数据库
      results = await searchDatabase(searchQuery.value)
      break
    case 'allDb':
      // 获取所有数据库记录
      results = await getAllDatabaseRecords()
      break
    default:
      // 搜索所有来源
      const [dbResults, addgeneResults] = await Promise.all([
        searchDatabase(searchQuery.value),
        axios.get(`${api.searchData}?q=${searchQuery.value}`).then(res => res.data)
      ])
      results = dbResults.concat(addgeneResults.data)
      pubsub.publish('filter-loading', false)
  }

  // 发布搜索结果
  pubsub.publish('getData', results)
  // pubsub.publish('loading', false) // Emit loading event
}

// 重置筛选
const resetFilters = () => {
  searchQuery.value = ''
  selectedTypes.value = []
  selectedCategories.value = []
  selectedSpecies.value = []
  searchMode.value = 'all'
}
</script>

<style lang="less" scoped>
.filter-card {
  position: sticky;
  top: 128px;
  
  :deep(.v-list-group__items) {
    padding-left: 16px;
  }

  :deep(.v-btn) {
    text-transform: none;
    letter-spacing: 0.5px;
  }

  .gap-2 {
    gap: 8px;
  }

  .cursor-pointer {
    cursor: pointer;
  }
}
</style>