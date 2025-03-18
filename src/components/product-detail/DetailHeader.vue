<template>
  <v-card class="mb-6">
    <v-card-text>
      <div class="d-flex flex-wrap align-start gap-6">
        <!-- 左侧图片 -->
        <div class="flex-shrink-0">
          <v-img
            :width="200"
            :aspect-ratio="1"
            cover
            class="bg-grey-lighten-2"
            :src="item.img"
          >
            <template v-slot:placeholder>
              <div class="d-flex align-center justify-center fill-height">
                <v-icon
                  icon="mdi-dna"
                  size="100"
                  color="grey-lighten-1"
                ></v-icon>
              </div>
            </template>
          </v-img>
        </div>

        <!-- 右侧信息 -->
        <div class="flex-grow-1">
          <h1 class="text-h4 font-weight-bold mb-2">{{ item.name }}</h1>
          <div class="d-flex flex-wrap gap-2 mb-4">
            <v-chip
              color="primary"
              size="small"
            >
              {{ item.category }}
            </v-chip>
            <v-chip
              variant="outlined"
              size="small"
            >
              {{ item.type }}
            </v-chip>
          </div>
          <p class="text-subtitle-1 mb-4">{{ item.description }}</p>
          <div class="d-flex flex-wrap gap-4">
            <div class="text-caption">
              <v-icon size="small" class="mr-1">mdi-account</v-icon>
              提交者：{{ item.depositor }}
            </div>
            <div class="text-caption">
              <v-icon size="small" class="mr-1">mdi-eye</v-icon>
              {{ item.views }} 次浏览
            </div>
            <div class="text-caption">
              <v-icon size="small" class="mr-1">mdi-file-document</v-icon>
              {{ item.publication }}
            </div>
          </div>
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { VCard, VCardText, VImg, VChip, VIcon } from 'vuetify/components'


defineProps({
  item: Object
})
</script>

<style lang="less" scoped>
.gap-2 {
  gap: 8px;
}

.gap-4 {
  gap: 16px;
}

.gap-6 {
  gap: 24px;
}
</style> 