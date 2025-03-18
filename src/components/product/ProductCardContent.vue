<template>
  <v-card-text class="px-0 py-4">
    <div class="text-subtitle-1 mb-2">{{ item.title }}</div>
    <div class="description">{{ item.description }}</div>
    <!-- <div class="mt-3 text-caption">
      <v-icon size="small" class="mr-1">mdi-eye</v-icon>
      {{ item.views }} 次浏览
    </div> -->
  </v-card-text>
</template>

<script setup>
import { VCardText, VIcon } from 'vuetify/components'

defineProps({
  item: Object
})
</script>

<style lang="less" scoped>
.description {
  color: rgba(0, 0, 0, 0.7);
  line-height: 1.6;
  max-height: 4.8em;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}
</style> 