<template>
  <v-card class="mx-auto news-card" elevation="2" height="100%">
    <v-img :src="item.image" height="300" cover></v-img>
    <div class="pa-6">
      <v-card-title class="text-h5 px-0">{{ item.title }}</v-card-title>
      <v-card-subtitle class="px-0 pt-2 text-subtitle-2">{{ item.date }}</v-card-subtitle>
      <v-card-text class="px-0 text-body-1">{{ item.description }}</v-card-text>
      <v-card-actions class="px-0">
        <v-spacer></v-spacer>
        <v-btn color="primary" variant="elevated" class="mb-2">
          了解更多
        </v-btn>
        <v-spacer></v-spacer>
      </v-card-actions>
    </div>
  </v-card>
</template>

<script setup>
import { VCard, VImg, VCardTitle, VCardSubtitle, VCardText, VCardActions, VSpacer, VBtn } from 'vuetify/components'

defineProps({
  item: {
    type: Object,
    required: true
  }
})
</script>

<style lang="less" scoped>
.news-card {
  transition: transform 0.3s ease;
  border-radius: 8px;
  overflow: hidden;
  
  &:hover {
    transform: translateY(-5px);
  }

  .v-card-title {
    font-weight: 600;
    line-height: 1.4;
  }

  .v-card-subtitle {
    opacity: 0.8;
  }

  .v-card-text {
    line-height: 1.8;
    margin-top: 12px;
  }
}
</style> 