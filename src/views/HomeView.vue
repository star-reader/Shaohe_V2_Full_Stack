<template>
  <div class="home-view">
    <home-carousel />
    <v-container class="news-section">
      <v-row>
        <v-col cols="12" class="text-center mb-12">
          <h2 class="text-h3 font-weight-bold">最新消息</h2>
          <p class="text-subtitle-1">关注我们的最新动态</p>
        </v-col>
      </v-row>
      <v-row>
        <v-col
          v-for="(news, index) in newsItems"
          :key="index"
          cols="12"
          md="6"
        >
          <news-card :item="news" />
        </v-col>
      </v-row>
    </v-container>

    <v-container class="progress-section">
      <v-row>
        <v-col cols="12" class="text-center mb-12">
          <h2 class="text-h3 font-weight-bold">生物学进展</h2>
          <p class="text-subtitle-1">探索生命科学的前沿发现</p>
        </v-col>
      </v-row>
      <v-row>
        <v-col
          v-for="(progress, index) in progressItems"
          :key="index"
          cols="12"
          md="6"
        >
          <news-card :item="progress" />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { VContainer, VRow, VCol } from 'vuetify/components'
import HomeCarousel from '@/components/home/HomeCarousel.vue'
import NewsCard from '@/components/home/NewsCard.vue'
import { newsItems } from '@/config/news'
import { progressItems } from '@/config/progress'
</script>

<style lang="less" scoped>
.news-section {
  padding: 100px 24px;
  
  .v-row {
    margin: 0;
  }
}

.progress-section {
  padding: 100px 24px;
  background-color: #f8f9fa;
  
  .v-row {
    margin: 0;
  }
}

.text-h3 {
  color: #1a237e;
  margin-bottom: 16px;
}

.text-subtitle-1 {
  color: #666;
  font-size: 1.2rem;
}
</style> 