<template>
  <div class="hero-section">
    <div class="hero-overlay"></div>
    <v-row class="fill-height" align="center" justify="center">
      <v-col cols="12" class="text-center">
        <h1 class="text-h1 font-weight-bold mb-6">微曦生物积木数据库</h1>
        <p class="text-h4 mb-8">生物技术领域的最新突破</p>
        <p class="text-h6 mb-16">生物积木的DNA元件库和菌株库实体会坐落在海珠区海纳产业园A栋411房</p>
        <v-row justify="center" class="mt-16">
          <v-col cols="12" sm="10" md="8" lg="6">
            <v-text-field
              v-model="searchQuery"
              prepend-inner-icon="mdi-magnify"
              placeholder="搜索生物积木..."
              variant="solo"
              hide-details
              class="search-input"
              bg-color="rgba(255, 255, 255, 0.9)"
              density="comfortable"
              @keyup.enter="handleSearch"
            >
              <template v-slot:append>
                <v-btn
                  color="primary"
                  class="search-btn"
                  @click="handleSearch"
                  size="large"
                >
                  搜索
                </v-btn>
              </template>
            </v-text-field>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { VRow, VCol, VTextField, VBtn } from 'vuetify/components'

const router = useRouter()
const searchQuery = ref('')

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      name: 'product',
      query: {
        q: searchQuery.value.trim()
      }
    })
  }
}
</script>

<style lang="less" scoped>
.hero-section {
  height: 100vh;
  background-image: url('@/assets/home/1.jpg');
  background-size: cover;
  background-position: center;
  position: relative;
  display: flex;
  align-items: center;

  .hero-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
  }

  .v-row {
    position: relative;
    z-index: 1;
    width: 100%;
    margin: 0;
  }

  h1, p {
    color: white;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
  }
}

.search-input {
  :deep(.v-field__append-inner) {
    padding-right: 0;
  }
  
  :deep(.v-field__input) {
    font-size: 1.2rem;
    min-height: 60px;
    padding: 0 20px;
  }

  :deep(.v-field__prepend-inner) {
    font-size: 1.5rem;
    padding-left: 12px;
  }
}

.search-btn {
  height: 100%;
  border-radius: 0 4px 4px 0;
  font-size: 1.1rem;
  padding: 0 32px;
  text-transform: none;
}
</style> 